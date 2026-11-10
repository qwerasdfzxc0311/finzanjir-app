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
