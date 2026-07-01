# Badge Activation

Tradar badges follow the ForestMate rule: badges should point at live provider-backed surfaces, not guessed status.

## Active or repo-activated

| Surface | Provider | Activation |
|---|---|---|
| Latest release | GitHub Releases | `https://github.com/spcx0701/tradar/releases/latest` becomes valid when a release tag is published. |
| Build | GitHub Actions | `.github/workflows/ci.yml` runs on `main` and pull requests. |
| GitHub Pages service | GitHub Pages | `CI / pages` deploys `app/` to `https://spcx0701.github.io/tradar/`. |
| CodeQL | GitHub code scanning | `.github/workflows/codeql.yml` runs on push, pull request, weekly schedule, and manual dispatch. |
| OpenSSF Scorecard | OpenSSF | `.github/workflows/scorecard.yml` publishes Scorecard results and uploads SARIF. |
| License | Repository | `LICENSE` is MIT. |
| PWA/data/AI/charts | Repository | Static repository/product claims backed by source files and docs. |

## Not displayed until provider-backed

| Surface | Why it is not in the README yet |
|---|---|
| Codecov | The repository did not have a valid `CODECOV_TOKEN`/Codecov provider setup at setup time; tokenless upload was rejected. |
| CodeFactor | The `spcx0701/tradar` project was not registered/analyzed by CodeFactor at setup time. |
| SonarCloud | The `spcx0701_tradar` SonarCloud component did not exist at setup time. |
| OpenSSF Best Practices | Tradar did not have its own Best Practices project id at setup time. Do not reuse ForestMate's project id. |
| REUSE API | The `github.com/spcx0701/tradar` REUSE API project was not registered at setup time. |
| Store badges | There was no verified Google Play, F-Droid, Obtainium, or other store listing for Tradar at setup time. |
