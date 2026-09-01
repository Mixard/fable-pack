---
name: expo-subscriptions
description: Use when implementing auto-renewable subscriptions, a free tier, or a bring-your-own-API-key option in an Expo/React Native app for iOS and Android, with server-side verification on Cloudflare Workers. Covers RevenueCat vs direct StoreKit 2/Play Billing, exact SDK call shapes, sandbox timing, App Store Server API and Play Developer API verification, and 2026 store policy.
---

# Expo subscriptions (StoreKit 2 + Play Billing + Cloudflare Workers, 2026)

RevenueCat publishes its own official Claude Code skill pack (`RevenueCat/ai-toolkit`, MIT/Apache-2.0, plus a hosted MCP server at `mcp.revenuecat.ai/mcp`) with deep per-platform SDK skills — install it for SDK-integration depth. This skill covers what that pack doesn't: the RevenueCat-vs-direct decision, Expo-specific wiring, Cloudflare Workers server-side verification, free-tier/BYOK architecture, and dated 2026 policy.

## Decision: RevenueCat vs direct (expo-iap / react-native-iap, OpenIAP)

| Dimension | RevenueCat (`react-native-purchases`) | Direct (`expo-iap` / `react-native-iap`) |
|---|---|---|
| Expo setup | `expo-dev-client` + `react-native-purchases`(+`-ui`); no config plugin; previews via a JS-mocked "Preview API Mode" in Expo Go, real purchases need a dev build | `expo-iap` is an Expo Module (native module — Expo Go compatibility not documented by the maintainers as of this research, presumed to need a dev build like other native Expo Modules); `react-native-iap` explicitly does **not** run in Expo Go **or** an Expo dev client — use `expo-iap` for any Expo project |
| Cross-platform entitlements | Built-in Offerings → Packages → StoreProduct, and CustomerInfo → EntitlementInfo, synced across iOS/Android/Amazon/Galaxy/Web | None provided — raw per-store products; you design the entitlement layer |
| Server-side verification | RevenueCat's backend verifies receipts/tokens and pushes you `CustomerInfo`/webhooks | You verify JWS (Apple) and tokens (Google) yourself — see below |
| Extra storefronts | Amazon Appstore, Samsung Galaxy Store, Web via Stripe (RevenueCat Billing) | Apple + Google core; `expo-iap` adds optional Meta Horizon/Fire OS/Vega OS/Onside plugins |
| Current version (2026-09) | v10 (10.8.1, ~weekly releases) | `expo-iap` 5.5.0 / `react-native-iap` 16.5.0 — both moved into the `hyodotdev/openiap` monorepo (old repos archived 2026-08-04, not abandoned), StoreKit 2 + Play Billing 9.1.0 |
| Pick this when | You want paywalls/experiments/a dashboard and don't want to run your own entitlement server | You want minimal third-party dependency in the purchase path, or need a StoreKit 2/Billing feature RevenueCat hasn't wrapped yet |

## RevenueCat on Expo — exact shapes

```ts
import Purchases, { PURCHASES_ERROR_CODE } from 'react-native-purchases';

Purchases.configure({ apiKey: Platform.OS === 'ios' ? IOS_KEY : ANDROID_KEY }); // appUserID optional -> anonymous ID

const isPro = (await Purchases.getCustomerInfo()).entitlements.active['pro'] !== undefined;

try {
  const { customerInfo } = await Purchases.purchasePackage(aPackage); // positional arg, NOT {aPackage}
} catch (e: any) {
  if (e.code !== PURCHASES_ERROR_CODE.PURCHASE_CANCELLED_ERROR) showError(e); // e.userCancelled is deprecated
}

await Purchases.restorePurchases(); // user-triggered only (can show OS sign-in); use syncPurchases() to restore programmatically
```
`PurchasesConfiguration` also takes `purchasesAreCompletedBy`, `entitlementVerificationMode`, `pendingTransactionsForPrepaidPlansEnabled`, `diagnosticsEnabled` (all optional). Gotcha: Billing Library 8+ removed querying *consumed* one-time purchases — anonymous users who bought consumables before switching devices can no longer restore them (affects `react-native-purchases` 9.0.0+).

## Apple — StoreKit 2 / App Store Server

- StoreKit 1 ("Original API for In-App Purchase") is marked deprecated in Apple's docs; **no published hard cutoff date** exists (unlike Google's). App Store Server Notifications **V1** specifically is explicitly deprecated — implement V2.
- Status endpoint: `GET https://api.storekit.apple.com/inApps/v1/subscriptions/{anyTransactionId}` (any transaction/original-transaction/app-transaction ID), optional repeated `?status=`, JWT-bearer authenticated (signed with your App Store Connect In-App Purchase key). Returns `status`: `1` active, `2` expired, `3` billing retry, `4` billing grace period, `5` revoked.
- App Store Server Notifications V2: POST webhook, body is a JWS `signedPayload`; decoded payload carries `notificationUUID` for de-duplication, and (in the transaction) `inAppOwnershipType` ("purchased" vs Family Sharing), `offerType` (`introductory`/`promotional`/`code`/`winBack`), `offerDiscountType`, `transactionReason`.
- `Product.displayPrice: String` — localized display price; use `price: Decimal` for math.
- Manage subscriptions in-app: `AppStore.showManageSubscriptions(in: UIWindowScene)` (iOS/iPadOS 15+; not for Mac Catalyst/Apple silicon Mac).
- Restore requirement (Guideline 3.1.1): "you should make sure you have a restore mechanism for any restorable in-app purchases."

Sandbox accelerated renewal (default "5 minute" speed; 3 other speeds selectable per Sandbox Apple Account):

| Duration | Renews every | Billing retry | Billing grace period |
|---|---|---|---|
| 1 week | 3 min | 10 min | 3 min |
| 1 month | 5 min | 10 min | 5 min |
| 2 months | 10 min | 10 min | 5 min |
| 3 months | 15 min | 10 min | 5 min |
| 6 months | 30 min | 10 min | 5 min |
| 1 year | 1 hour | 10 min | 5 min |

A sandbox subscription auto-renews up to 12 times, then stops on the 13th attempt.

## Google — Play Billing Library / Play Developer API

Version enforcement (2-year cycle per version; deadlines confirmed live 2026-09-01, the day after v7's deadline hit):

| Version | New app/update deadline | Extension deadline |
|---|---|---|
| 7 | 2026-08-31 (in force now) | 2026-11-01 |
| 8 (current floor) | 2027-08-31 | 2027-11-01 |
| 9 (latest, 9.1.0) | 2028-08-31 | 2028-11-01 |

Breaking changes landed in Billing Library 8.0.0 (2025-06-30): `SkuDetails`/`querySkuDetailsAsync()` **removed** (use `ProductDetails`/`queryProductDetailsAsync()`); the no-arg `enablePendingPurchases()` overload **removed** — you must now pass `PendingPurchasesParams` explicitly, and calling it remains mandatory, not automatic; the `queryPurchasesAsync(String skuType, listener)` overload removed; `queryPurchaseHistory()` removed; "in-app items" renamed "one-time products." In 9.0.0, a blocked Play Store app now returns `BILLING_UNAVAILABLE` instead of `ERROR`.

Verification: `GET https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{packageName}/purchases/subscriptionsv2/tokens/{token}` returns `subscriptionState`: `SUBSCRIPTION_STATE_{ACTIVE, PENDING, PAUSED, IN_GRACE_PERIOD, ON_HOLD, CANCELED, EXPIRED, PENDING_PURCHASE_CANCELED, UNSPECIFIED}`. Real-time developer notifications arrive via Pub/Sub as a base64 `DeveloperNotification`; Google's own doc: "These notifications tell you only that the purchase state changed. They do not give you complete information about the purchase" — always re-fetch via the endpoint above; de-duplicate on the Pub/Sub `messageId`.

Subscriptions are structured as one product with multiple **base plans**, each with optional **offers**. Account hold defaults to enabled, auto-calculated as **60 days minus the grace period**; total of grace period + account hold must be ≥30 days (exact default grace-period day count is not published — see Unverified). Default price-increase flow is opt-in: subscribers get a 30-day notice before a 37-day-out charge, or auto-cancel; a no-action opt-out variant exists in some cases with a 30- or 60-day notice. License testers (Play Console → Settings → License testing) get named test instruments (always-approve, always-decline, slow-approve/decline, charge-back) that use the real purchase UI without moving money.

## Server-side verification on Cloudflare Workers

- Apple's official `@apple/app-store-server-library` (Node) depends on `jsonwebtoken`/`node-fetch` — Node-oriented. Cloudflare's `nodejs_compat` flag (which enables `node:crypto`) is **on by default for compatibility dates ≥ 2026-08-04**; on an older pinned date, set it explicitly. Alternative: Workers' native `crypto.subtle` (Web Crypto) supports RSASSA-PKCS1-v1_5 (RS256) sign/verify directly, enough to hand-verify Apple's JWS chain with zero Node dependency.
- Google service-account calls to the Play Developer API don't need the Node `googleapis` SDK either: build a JWT (`iss`=service-account email, `scope`, `aud`=`https://oauth2.googleapis.com/token`, `iat`, `exp`), sign it RS256 via `crypto.subtle`, POST to that token endpoint with `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer`, use the returned bearer token against `androidpublisher.googleapis.com`.
- Idempotency: Apple's decoded notification carries `notificationUUID` explicitly for de-dup; Google's Pub/Sub message carries `messageId` (Google recommends checking uniqueness). Treat both notification channels as unreliable-delivery signals, not state — always confirm against the status endpoints below before writing entitlements.

Verification endpoints to call from your Worker:
- Apple status: `GET https://api.storekit.apple.com/inApps/v1/subscriptions/{transactionId}`
- Apple webhook: App Store Server Notifications V2 (you receive `signedPayload` JWS at a URL you register in App Store Connect)
- Google status: `GET https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{packageName}/purchases/subscriptionsv2/tokens/{token}`
- Google webhook: RTDN via Pub/Sub (push subscription to your Worker, or pull)

## Free tier and bring-your-own-API-key (BYOK)

Free tier needs no special API: gate features on entitlement absence (`entitlements.active['pro'] === undefined`). BYOK (user supplies their own key to a third-party provider, e.g. their own LLM API key) typically involves **no IAP transaction at all** — store the key locally (e.g. `expo-secure-store`), call the provider directly from the device, and there is nothing to verify server-side because the developer isn't selling the unlocked access. Whether this reliably sidesteps Guideline 3.1.1's requirement to "use in-app purchase" to unlock features or functionality is a reasonable, common pattern but not something Apple has ruled on publicly for BYOK specifically — see Unverified.

## Policy (dated)

| Date | Event |
|---|---|
| 2025-12-11 | 9th Circuit rejects both Apple's flat 27% and the district court's $0 commission on US external-link purchases; remands for a "reasonable, non-prohibitive" figure |
| 2026-06-30 | Supreme Court grants cert on Apple's contempt-finding appeal; argued in the term starting Oct 2026 — no ruling expected in 2026 |
| 2026-09-01 | Underlying injunction still in force: Apple's own Guideline 3.1.1(a) confirms no entitlement is needed for external purchase links/buttons on the **US** storefront; **the commission Apple may charge on those purchases is unsettled** — do not hardcode a rate |
| ongoing | Google Play **User Choice Billing**: 4-percentage-point service-fee reduction in most eligible regions, 35+ countries, category rules vary by region (any category in EEA and Japan; non-gaming elsewhere, with gaming carve-ins for South Korea/India/US; US fee reduction varies by program rather than a flat 4 points) |

Apple requires, on every storefront: a restore mechanism (Guideline 3.1.1) and clear subscription-terms disclosure (Guideline 3.1.2(c) → Developer Program License Agreement Schedule 2). No equivalent numbered Google Play guideline was found in this research, but on both platforms subscriptions remain manageable via the platform's own account settings regardless of in-app UI.

## Gotchas

- `Purchases.purchasePackage(pkg)` is a **positional** call in the RN SDK — some doc snippets showing `{ aPackage: pkg }` are a different platform binding (likely Capacitor); trust the TS source over an unlabeled doc code tab.
- `PurchasesError.userCancelled` is deprecated; compare `error.code === PURCHASES_ERROR_CODE.PURCHASE_CANCELLED_ERROR`.
- `react-native-iap` v14+ requires Nitro Modules (`react-native-nitro-modules`) and RN 0.79+; pin `react-native-iap@13.1.0` if stuck on older RN.
- RTDN/App Store Server Notifications are delivery-unreliable signals, never a state source — always re-verify via the status endpoints.
- A repo showing "archived" for `expo-iap`/`react-native-iap` (moved to `hyodotdev/openiap`, Aug 2026) does not mean abandoned — check the monorepo's release dates instead.

## Unverified (do not assert as fact without re-checking)

- Exact commission Apple currently charges on US external-link purchases post-remand — actively relitigated.
- StoreKit 1 / `verifyReceipt` hard cutoff date — none published as of this research; only "deprecated."
- `expo-iap`'s minimum Expo SDK version and its own Expo Go compatibility (unlike RevenueCat's documented "Preview API Mode," no equivalent statement was found for `expo-iap`).
- Exact default grace-period day count on Google Play (only the account-hold-minus-grace-period *formula* is documented, not grace period's own default).
- A specific Google Play policy sentence mandating an in-app "manage/cancel subscription" link (Apple's nearest anchor is 3.1.2(c) plus the `showManageSubscriptions` API, not a numbered guideline).
- Whether BYOK specifically is exempt from Guideline 3.1.1 — architectural inference, not a quoted Apple ruling.

## Sources

RevenueCat: revenuecat.com/docs (installation/expo, getting-started/configuring-sdk, making-purchases, restoring-purchases, offerings/overview), github.com/RevenueCat/react-native-purchases, github.com/RevenueCat/purchases-hybrid-common, github.com/RevenueCat/ai-toolkit, github.com/RevenueCat/play-billing-skills, mcp.revenuecat.ai/mcp.
expo-iap / react-native-iap: github.com/hyodotdev/openiap (libraries/expo-iap, libraries/react-native-iap), openiap.dev, registry.npmjs.org.
Apple: developer.apple.com/documentation/storekit, developer.apple.com/documentation/appstoreserverapi, developer.apple.com/documentation/appstoreservernotifications, developer.apple.com/app-store/review/guidelines, developer.apple.com/help/app-store-connect/test-in-app-purchases.
Google: developer.android.com/google/play/billing (compatibility, release-notes, rtdn-reference, subscriptions, lifecycle/subscriptions, price-changes, test, alternative), developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2, support.google.com/googleplay/android-developer.
Server-side: github.com/apple/app-store-server-library-node, developers.cloudflare.com/workers/runtime-apis (nodejs, web-crypto), developers.google.com/identity/protocols/oauth2/service-account.
Policy/litigation: developer.apple.com/app-store/review/guidelines, fenwick.com (Ninth Circuit analysis), macrumors.com (2026-06-30 SCOTUS cert).
