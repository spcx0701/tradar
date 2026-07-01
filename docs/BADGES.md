# Badge Activation

Tradar badges follow the ForestMate rule: badges should point at live provider-backed surfaces, not guessed status.

## Active or repo-activated

| Surface | Provider | Activation |
|---|---|---|
| Latest release | GitHub Releases | `https://github.com/spcx0701/tradar/releases/latest` becomes valid when a release tag is published. |
| Build | GitHub Actions | `.github/workflows/ci.yml` runs on `main` and pull requests. |
| CodeQL | GitHub code scanning | `.github/workflows/codeql.yml` runs on push, pull request, weekly schedule, and manual dispatch. |
| OpenSSF Scorecard | OpenSSF | `.github/workflows/scorecard.yml` publishes Scorecard results and uploads SARIF. |

## Not displayed until provider-backed

| Surface | Why it is not in the README yet |
|---|---|
| Codecov coverage | `CI / test` generates `coverage.xml`, but Codecov OIDC upload returned `Repository not found` and the badge still reports `coverage: unknown`. Add/enable the `spcx0701/tradar` repository in Codecov before displaying the badge. |
| CodeFactor | The `spcx0701/tradar` project was not registered/analyzed by CodeFactor at setup time. |
| SonarCloud | The `spcx0701_tradar` SonarCloud component did not exist at setup time. |
| GitHub Code Quality | GitHub's Code Quality setup API returned `Code quality is not available for this repository.` |
| OpenSSF Best Practices | Tradar did not have its own Best Practices project id at setup time. Do not reuse ForestMate's project id. |
| REUSE API | The `github.com/spcx0701/tradar` REUSE API project was not registered at setup time. |
| Store badges | There was no verified Google Play, F-Droid, Obtainium, or other store listing for Tradar at setup time. |
| Product/static badges | Language, license, service, PWA, data, AI, and chart-library badges are intentionally omitted from the README badge row. |
