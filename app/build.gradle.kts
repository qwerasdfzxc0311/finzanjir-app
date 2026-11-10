import java.security.MessageDigest

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "uz.finzanjir.mobile"
    compileSdk = 35
    defaultConfig {
        applicationId = "uz.finzanjir.mobile"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    testBuildType = "candidate"
    buildTypes {
        release { isMinifyEnabled = false }
        create("candidate") {
            initWith(getByName("debug"))
            applicationIdSuffix = ".candidate"
            versionNameSuffix = "-candidate"
            matchingFallbacks += listOf("debug")
        }
    }
    buildFeatures { compose = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

val candidatePartFiles = (1..12).map { index ->
    rootProject.file(
        "source-import/candidates/finzanjir_knowledge_merged_6679_part_%02d.json".format(index)
    )
}
val candidateAssetsDir = layout.buildDirectory.dir("generated/candidateKnowledgeAssets")
val prepareCandidateKnowledgeAssets = tasks.register("prepareCandidateKnowledgeAssets") {
    inputs.files(candidatePartFiles)
    outputs.dir(candidateAssetsDir)
    doLast {
        require(candidatePartFiles.all { it.isFile }) {
            "FINZANJIR 6,679 candidate corpus is incomplete"
        }
        val outputDir = candidateAssetsDir.get().asFile
        outputDir.mkdirs()
        val mergedFile = outputDir.resolve("finzanjir_knowledge.json")
        mergedFile.bufferedWriter(Charsets.UTF_8).use { writer ->
            writer.append("[")
            var first = true
            candidatePartFiles.forEach { part ->
                val raw = part.readText(Charsets.UTF_8).trim()
                require(raw.startsWith("[") && raw.endsWith("]")) {
                    "Invalid candidate JSON array: ${part.name}"
                }
                val body = raw.substring(1, raw.length - 1).trim()
                if (body.isNotEmpty()) {
                    if (!first) writer.append(",")
                    writer.append(body)
                    first = false
                }
            }
            writer.append("]")
        }
        val sha = MessageDigest.getInstance("SHA-256")
            .digest(mergedFile.readBytes())
            .joinToString("") { "%02x".format(it) }
        outputDir.resolve("knowledge_manifest.json").writeText(
            """{"record_count":6679,"asset_sha256":"$sha","knowledge_base_version":"candidate-6679-fts4"}""",
            Charsets.UTF_8
        )
    }
}

android.sourceSets.getByName("candidate").assets.srcDir(candidateAssetsDir)
tasks.named("preBuild").configure {
    dependsOn(prepareCandidateKnowledgeAssets)
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.12.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)
    implementation("androidx.activity:activity-compose:1.10.0")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.8.5")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    debugImplementation("androidx.compose.ui:ui-tooling")
    androidTestImplementation("androidx.test:runner:1.6.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
}
