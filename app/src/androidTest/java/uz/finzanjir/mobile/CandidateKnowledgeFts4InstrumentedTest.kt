package uz.finzanjir.mobile

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Runs only against the isolated .candidate application ID.
 * The 6,679-record corpus is generated into this variant's assets at build time;
 * the normal debug APK continues to use the original 1,121-record asset.
 */
@RunWith(AndroidJUnit4::class)
class CandidateKnowledgeFts4InstrumentedTest {

    @Test
    fun operationalModulesShareEventSignalCaseAndCitizenAuditState() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        context.getSharedPreferences("finzanjir_demo_workflow_v1", android.content.Context.MODE_PRIVATE)
            .edit().clear().commit()

        var snapshot = WorkflowStore.load(context)
        assertEquals("EVT-DEMO-0001", snapshot.eventId)
        assertEquals("SIG-DEMO-0001", snapshot.signalId)
        assertEquals("CASE-DEMO-0001", snapshot.caseId)

        listOf("RISK_ENGINE", "CROSS_MATCH", "FRAUD_GRAPH", "TIMELINE", "FIN_RECOVERY").forEach { stage ->
            snapshot = WorkflowStore.runStage(context, stage)
        }
        snapshot = WorkflowStore.runStage(context, "RISK_ENGINE")
        assertEquals(1, snapshot.records.count { it.type == "RISK_ASSESSMENT" })
        assertTrue(snapshot.records.any { it.id == "ENT-CARD-DEMO-0001" })
        assertTrue(snapshot.records.any { it.type == "GRAPH_EDGE" })
        assertTrue(snapshot.records.any { it.type == "RECOVERY_CASE" })

        (snapshot.records + snapshot.audit).forEach { record ->
            assertEquals(snapshot.eventId, record.eventId)
            assertEquals(snapshot.signalId, record.signalId)
            assertEquals(snapshot.caseId, record.caseId)
        }
        assertTrue(snapshot.records.filter { it.type in setOf("RISK_ASSESSMENT", "CROSS_MATCH", "GRAPH_NODE", "GRAPH_EDGE", "TIMELINE", "RECOVERY_CASE") }
            .all { it.relatedIds.isNotEmpty() })

        snapshot = WorkflowStore.updateCitizenCardStatus(context, "UNKNOWN")
        assertEquals("UNKNOWN", snapshot.records.first { it.type == "CITIZEN_CARD" }.status)
        assertTrue(snapshot.audit.any { it.title.contains("karta holatini") })

        snapshot = WorkflowStore.recordReview(context, "MORE_INFORMATION", "Dalil manbasini qayta tekshirish kerak.")
        assertEquals("MORE_INFORMATION", snapshot.reviewStatus)
        assertTrue(snapshot.records.any { it.type == "HUMAN_REVIEW" })
        assertTrue(snapshot.audit.isNotEmpty())
    }

    @Test
    fun importsFullCandidateCorpusAndRetrievesCoreModules() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext

        val importedCount = FinzanjirKnowledgeBase.count(context)
        assertEquals("Candidate corpus import count", 6679, importedCount)

        val questions = listOf(
            "Risk Engine nima?",
            "Cross-Match nima?",
            "Fraud Graph nima?",
            "Timeline qanday ishlaydi?",
            "FIN-RECOVERY nima?",
            "Mening kartalarim nima?"
        )

        questions.forEach { question ->
            val result = FinzanjirKnowledgeBase.search(
                context = context,
                question = question,
                expertMode = true
            )
            assertEquals("$question: imported row count", 6679, result.recordCount)
            assertFalse("$question: answer must not be empty", result.answer.isBlank())
            assertTrue("$question: FTS4 must return traceable sources", result.sources.isNotEmpty())
        }
    }
}
