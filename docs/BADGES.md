# Badge Activation

Tradar badges follow the ForestMate rule: badges should point at live provider-backed surfaces, not guessed status.

## Active or repo-activated

| Surface | Provider | Activation |
|---|---|---|
| Latest release | GitHub Releases | `https://github.com/spcx0701/tradar/releases/latest` becomes valid when a release tag is published. |
| Build | GitHub Actions | `.github/workflows/ci.yml` runs on `main` and pull requests. |
| CodeQL | GitHub code scanning | `.github/workflows/codeql.yml` runs on push, pull request, weekly schedule, and manual dispatch. |
| CodeFactor code quality | CodeFactor/Shields.io | The public repository review was requested through CodeFactor and the README uses a Shields badge labeled `code quality` for the live grade `B`. |
| Codecov coverage | Codecov | `CI / test` uploads `coverage.xml` with GitHub OIDC after the repository was connected in Codecov. |
| OpenSSF Scorecard | OpenSSF | `.github/workflows/scorecard.yml` publishes Scorecard results and uploads SARIF. |
| OpenSSF Best Practices | OpenSSF | Tradar is registered as Best Practices project `13452`; the live badge is updated from the provider edit form using repo-backed evidence. |
| SonarCloud | SonarCloud | The GitHub repository is imported as project key `spcx0701_tradewind` and exposes Bugs, Security Rating, Maintainability Rating, and Technical Debt badges. |
| Obtainium | Obtainium redirect | The README uses `https://apps.obtainium.page/redirect?r=obtainium://add/https://github.com/spcx0701/tradar`, which resolves and adds the GitHub repository as an Obtainium source. |
| Android GitHub Releases | GitHub Releases | The README links to `https://github.com/spcx0701/tradar/releases/latest`, verified to resolve to the latest release page. APK release assets still need a future release workflow/run before this becomes complete Android distribution proof. |

## Prepared but not provider-live

| Surface | Current status |
|---|---|
| Google Play | The README includes the package URL `https://play.google.com/store/apps/details?id=kr.tradewind.app` as a pre-listing link. Current verification returns `404`, so this must not be described as a live Play Store listing until Play Console publication makes the page reachable. |

## Not displayed until provider-backed

| Surface | Why it is not in the README yet |
|---|---|
| GitHub Code Quality | GitHub's Code Quality setup API returned `Code quality is not available for this repository.` |
| REUSE API | The `github.com/spcx0701/tradar` REUSE API project was not registered at setup time. |
| F-Droid | There is no verified F-Droid package or metadata listing for Tradar yet. |
| Product/static badges | Language, license, service, PWA, data, AI, and chart-library badges are intentionally omitted from the README badge row. |
