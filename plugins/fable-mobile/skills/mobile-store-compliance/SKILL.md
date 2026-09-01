---
name: mobile-store-compliance
description: Use when preparing a consumer Android or iOS app for Google Play or App Store submission in 2026 - a dated compliance calendar (target API level, Play Billing, developer verification, AccessibilityService, foreground services, privacy manifests, Xcode/SDK minimums) plus a checklist for apps using AI-generated text, an accessibility overlay, microphone, chat screenshots, and subscriptions.
---

# Mobile store compliance calendar (baseline: 2026-09-01)

Every row below was verified against a primary source (support.google.com/googleplay/android-developer,
developer.android.com, developer.apple.com) on 2026-09-01 - URL and a verbatim quote for each
row was checked against a primary source. Store policy dates move; this
skill is a strong candidate for the `freshness-sweep` rotation (re-verify pinned dates against
a live source before trusting anything here more than ~90 days out). Anything not confirmed
from a primary source is listed under Unverified, not folded into the tables.

## Google Play

| Date | Requirement | Detail | Source |
|---|---|---|---|
| 2021-11-03 | AccessibilityService declaration form | Apps targeting Android 12+ using the AccessibilityService API must pass Play's Permission Declaration Form before publishing | [answer/10964491](https://support.google.com/googleplay/android-developer/answer/10964491) |
| 2023-10-25 | AI-generated content: reporting requirement | Google requires "certain" genAI apps (subset undefined in the policy text) to ship in-app user reporting/flagging for AI-generated content — treat as applicable by default for a user-facing genAI text app | [answer/14016515](https://support.google.com/googleplay/android-developer/answer/14016515) |
| 2023-11-13 (cutoff) | Closed testing for new personal accounts | Personal accounts created after this date need 12 testers opted in continuously for 14 days before production access | [answer/14151465](https://support.google.com/googleplay/android-developer/answer/14151465) |
| Since target API 34 (Android 14) | Foreground service type + microphone declaration | Manifest `foregroundServiceType="microphone"` + `FOREGROUND_SERVICE_MICROPHONE`; Play Console needs a description, user-impact note, and demo video per FGS type | [answer/13392821](https://support.google.com/googleplay/android-developer/answer/13392821), [service types](https://developer.android.com/develop/background-work/services/fgs/service-types) |
| 2025-05-28 (in force) | Photo and Video Permissions enforced | Full compliance mandatory for `READ_MEDIA_IMAGES`/`READ_MEDIA_VIDEO`; broad/persistent access needs a core-use-case justification, else use the system photo picker | [answer/14115180](https://support.google.com/googleplay/android-developer/answer/14115180) |
| 2025-10-30 | AccessibilityService: autonomous actions banned | Using the API so the app "autonomously initiate[s], plan[s], and execute[s] actions" without the user's knowledge/consent is prohibited; static rule-based ("if X then Y") automation is exempt | [answer/16550159](https://support.google.com/googleplay/android-developer/answer/16550159) (ban announcement); exemption wording lives on [answer/10964491](https://support.google.com/googleplay/android-developer/answer/10964491) |
| 2026-08-31 (passed; ext. 2026-11-01) | Target API level 36 required | New apps and updates must target Android 16 (API 36); no 2027 level published yet | [answer/11926878](https://support.google.com/googleplay/android-developer/answer/11926878) |
| 2026-08-31 (passed; ext. 2026-11-01) | Play Billing Library v8 required | Apps selling in-app products/subscriptions must be on Billing Library 8+ | [deprecation FAQ](https://developer.android.com/google/play/billing/deprecation-faq) |
| 2026-09-30 | Android developer verification enforced (4 countries) | Apps need a verified developer identity to install on certified devices in Brazil, Indonesia, Singapore, Thailand (Play and other participating stores). This is NOT the Play D-U-N-S business-verification program - different requirement, different scope | [developer-verification](https://developer.android.com/developer-verification) |
| 2027 (no exact date yet) | Android developer verification goes global | Same program expands to all certified Android devices worldwide | [developer-verification](https://developer.android.com/developer-verification) |
| 2027-08-31 (ext. 2027-11-01) | Play Billing Library v9 required | Next Billing Library floor, already published | [deprecation FAQ](https://developer.android.com/google/play/billing/deprecation-faq) |
| Standing | Data safety form | Required on closed/open/production tracks; apps active exclusively on the internal testing track are exempt. Screenshots of chats disclose under "Photos and videos"; mic audio under "Voice or sound recordings"; sending data to an external AI API counts as a "service provider," not "sharing," only if it processes solely on your instructions | [answer/10787469](https://support.google.com/googleplay/android-developer/answer/10787469) |
| Standing | User Data policy | Disclosure must be transparent and precede the runtime permission prompt; apps with account creation must offer account deletion both in-app AND via an external web resource (URL entered in Play Console) | [answer/10144311](https://support.google.com/googleplay/android-developer/answer/10144311) |

## App Store

| Date | Requirement | Detail | Source |
|---|---|---|---|
| Since iOS 10.0 (2016) | Purpose strings required | `NSMicrophoneUsageDescription`, and `NSSpeechRecognitionUsageDescription` if using Apple's speech recognition, or the app is killed on first use without them; `NSPhotoLibraryUsageDescription` / `NSPhotoLibraryAddUsageDescription` likewise for chat-screenshot import | [Info.plist key reference](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html) |
| Since iOS 14.5 (2021) | App Tracking Transparency | Permission via the ATT framework required before tracking or reading the advertising identifier | [App Privacy & data use](https://developer.apple.com/app-store/user-privacy-and-data-use/) |
| Since WWDC23 (Jun 2023) | Privacy manifests + third-party SDK list | `PrivacyInfo.xcprivacy` required when submitting or updating an app that bundles any of 80+ listed SDKs (all Firebase*, FBSDK*, GoogleSignIn, Alamofire, AFNetworking, React Native/Flutter/Cordova deps, etc.); binary-dependency signatures required too | [third-party SDK requirements](https://developer.apple.com/support/third-party-SDK-requirements/) |
| 2026-04-28 (passed) | Xcode 26 / iOS 26 SDK minimum | Apps and games uploaded to App Store Connect must be built with the iOS 26 & iPadOS 26 SDK or later (tvOS/visionOS/watchOS 26 likewise). iOS 27 is not GA as of 2026-09-01 ("ships this fall" per Apple); no iOS 27 SDK minimum announced yet | [SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw) |
| 2026-06-08 | App Review Guidelines revision | Current baseline for every guideline row below; this revision directly touched 1.2 (UGC) and 4.3(a)/(b) (spam) | [Guidelines/DPLA update](https://developer.apple.com/news/?id=a233fmpw) |
| Standing (rev. 2026-06-08) | 1.2 User-Generated Content | Chat-like UGC needs a content filter, a report mechanism, the ability to block abusive users, and published contact info | [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Standing | 3.1.2 Auto-renewable subscriptions | Disclose price/duration/what's included before purchase; 7-day minimum period, usable on all the user's devices; no extra tasks (social posts, invites) required to get what was paid for | [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Standing | 5.1.1(v) Account deletion | Apps that support account creation must offer account deletion in-app | [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Standing | 4.8 Login Services | Third-party/social sign-in requires an equivalent privacy-preserving option; Sign in with Apple satisfies it. Exceptions: company-only accounts, alt-marketplace logins, education/enterprise/government-ID logins, direct clients of the third-party service itself | [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Standing (4.3 revised 2026-06-08; 5.1.2(i)/4.2.6 unchanged by that revision, current as of the same baseline) | 5.1.2(i), 4.2.6, 4.3 - AI content gates | No dedicated "AI-generated content" guideline exists; instead: disclose third-party AI data sharing with explicit permission (5.1.2(i)); apps from a commercialized template/generation service are rejected unless submitted by the content provider (4.2.6); apps indistinguishable from what's already on the Store are rejected as spam (4.3) | [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| Standing | TestFlight limits | 100 internal testers, 10,000 external testers, builds expire 90 days after upload | [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/) |
| Standing | App Privacy nutrition labels | Every submission/update must disclose data types collected - including by bundled third-party SDKs - and whether used for tracking | [App Privacy & data use](https://developer.apple.com/app-store/user-privacy-and-data-use/) |

## Before submission: checklist by feature

**AI-generated text**
- Play: ship in-app reporting/flagging for AI output; disclose the AI backend call in the Data safety form as a "service provider" (not "sharing") if it only processes on your instructions.
- App Store: disclose third-party AI data sharing with explicit permission (5.1.2(i)); confirm the app isn't rejectable as template/indistinguishable content (4.2.6/4.3); update the App Privacy label if AI processing changed what data leaves the device.

**AccessibilityService overlay** (Android-only feature; iOS has no equivalent third-party automation API)
- `isAccessibilityTool` is almost certainly unavailable - the app's core purpose isn't disability assistance - so prominent, in-app, consent-gated disclosure is mandatory before first use.
- Every automated action must be deterministic ("if X then Y"); do not let a model decide accessibility-API actions autonomously - explicitly banned since 2025-10-30.
- Complete the Permission Declaration Form before publishing.
- Re-verify current Restricted-settings / Enhanced Confirmation Mode behavior on a real device before depending on it for sideloaded QA builds - not confirmed this research cycle (see Unverified).

**Microphone**
- Declare `FOREGROUND_SERVICE_MICROPHONE` + runtime `RECORD_AUDIO`; the foreground service cannot be started while the app is backgrounded.
- File the Play Console FGS declaration: description, user-impact note, demo video.
- Disclose "Voice or sound recordings" in the Data safety form.
- Add `NSMicrophoneUsageDescription`, plus `NSSpeechRecognitionUsageDescription` if using Apple's speech recognition.

**Screenshots of chats**
- Prefer the system photo picker over broad `READ_MEDIA_IMAGES`; broad/persistent gallery access needs a core-use-case justification under the Photo and Video Permissions policy.
- Disclose under "Photos and videos" in the Data safety form.
- Add `NSPhotoLibraryUsageDescription` (or the Add-only variant if the app never reads existing photos).
- If imported screenshots surface other people's chat content inside your UI, guideline 1.2 (UGC) applies: a report mechanism and the ability to block abusive users.

**Subscriptions and accounts**
- Confirm Play Billing Library 8+ now; plan the migration to 9+ before 2027-08-31.
- Disclose price, duration, and included value before purchase; keep the subscription usable without extra tasks (3.1.2).
- Offer account deletion within the app on both stores; Play additionally requires an external web resource for account deletion, linked in Play Console (Play User Data policy; guideline 5.1.1(v), in-app only for Apple).
- If offering third-party/social sign-in, also offer Sign in with Apple (guideline 4.8).

**General, every submission**
- Confirm target API level 36 (Android 16) and Billing Library 8+ are both current before uploading.
- Confirm the build uses the iOS 26/iPadOS 26 SDK minimum (Xcode 26+).
- New/personal developer account: plan the 12-tester/14-day closed test before requesting production access.
- Distributing in Brazil, Indonesia, Singapore, or Thailand: register for Android developer verification well before the 2026-09-30 enforcement date.

## Unverified

Not confirmed against a primary source this research cycle - re-check before relying on these:

- Restricted settings (Android 13, blocks sensitive grants for sideloaded apps) is confirmed via support.google.com/android/answer/12623953 — outside this skill's usual domain list but Google-owned. "Enhanced Confirmation Mode" (the claimed Android 15 refinement) specifically has no findable primary source after exhaustive search across two research passes — treat that name/detail as unconfirmed, and its effect on a developer's own ADB/sideloaded debug builds during QA remains unknown either way.
- Export compliance (`ITSAppUsesNonExemptEncryption`): confirmed at developer.apple.com/documentation/security/complying-with-encryption-export-regulations (fetch the `.md` variant of the URL if your tool can't render the JS shell) — HTTPS/standard OS encryption is exempt from export documentation.
- EU DSA trader-status requirement: confirmed at developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements — Articles 30/31 require declaring trader status even if you don't distribute in the EU.
- Privacy manifest required-reason-API enforcement date: confirmed as 2024-05-01 at developer.apple.com/news/?id=3d8a9yyh ("Starting May 1: You'll need to include approved reasons..."). The specific rejection code ITMS-91053 remains unconfirmed against any Apple-authored page (only developer-forum quotes of their own rejection emails).
- Play closed-testing history: confirmed — the requirement was 20 testers (announced Nov 2023) before Google reduced it to 12 on Dec 11, 2024, per android-developers.googleblog.com/2023/11/ensuring-high-quality-apps-on-google-play.html.
