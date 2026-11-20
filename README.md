# CHERRY AI Android starter

This is a personal-use starter APK project.

## Features in this first build
- Pink/purple Kivy interface
- Tamil, Telugu and English language selector
- ElevenLabs text-to-speech using a Voice ID you provide
- API key is typed at runtime and is not included in the APK source

## Current limitations
- This first build speaks text that you type. Android microphone speech recognition and a conversational AI backend are not implemented yet.
- Choose an ElevenLabs voice that is suitable for Tamil, Telugu and English. A voice's gender/softness is determined by the Voice ID you choose, not by this app.
- Eleven v3 supports Tamil and Telugu. Availability and usage depend on your ElevenLabs account.
- Keep this APK for your own testing. Do not share an APK while using your personal API key; a production app should call a protected server that holds the key.

## Build from an Android phone using GitHub Actions
1. Download and extract `CHERRY_AI_Android_Project.zip` on your phone.
2. Sign in to GitHub in your phone browser and create a new repository.
3. Upload the extracted project contents, including the `.github/workflows/build-apk.yml` file and folder structure.
4. Open the repository's Actions tab.
5. Select `Build CHERRY AI APK` and tap `Run workflow`.
6. Wait for the workflow to finish successfully.
7. Open the completed workflow run, scroll to Artifacts, and download `cherry-ai-debug-apk`.
8. Extract the artifact ZIP, tap the APK, and follow Android's install prompt. Only install APKs you built or trust.

The workflow builds a debug APK. It is for testing, not a Play Store release.
