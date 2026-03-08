# Contributors action

> [!IMPORTANT]
> This repository has moved from `github/contributors` to `github-community-projects/contributors`.
> Please update your git remote:
>
> ```shell
> git remote set-url origin git@github.com:github-community-projects/contributors.git
> ```
>
> Note: replace `origin` with the name of your remote if it's different.

[![Python package](https://github.com/github-community-projects/contributors/actions/workflows/python-ci.yml/badge.svg)](https://github.com/github-community-projects/contributors/actions/workflows/python-ci.yml)
[![Docker Image CI](https://github.com/github-community-projects/contributors/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/github-community-projects/contributors/actions/workflows/docker-ci.yml)
[![CodeQL](https://github.com/github-community-projects/contributors/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/github-community-projects/contributors/actions/workflows/github-code-scanning/codeql)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/github-community-projects/contributors/badge)](https://scorecard.dev/viewer/?uri=github.com/github-community-projects/contributors)

This is a GitHub Action that given an organization or specified repositories, produces information about the [contributors](https://chaoss.community/kb/metric-contributors/) over the specified time period.

Similar actions to help you recognize contributors by putting them into a `README` or `CONTRIBUTORS.md` include:

- [contributor-list](https://github.com/marketplace/actions/contribute-list)

This action was developed by the GitHub OSPO for our own use and developed in a way that we could open source it that it might be useful to you as well! If you want to know more about how we use it, reach out in an issue in this repository.

## Example use cases

- As a maintainer, you may want to acknowledge recent contributors in a discussion post
- As an OSPO or maintainer, you may want to know who candidates are for new maintainers

## Support

If you need support using this project or have questions about it, please [open up an issue in this repository](https://github.com/github-community-projects/contributors/issues). Requests made directly to GitHub staff or support team will be redirected here to open an issue. GitHub SLA's and support/services contracts do not apply to this repository.

### OSPO GitHub Actions as a Whole

All feedback regarding our GitHub Actions, as a whole, should be communicated through [issues on our github-ospo repository](https://github.com/github/github-ospo/issues/new).

## What is a contributor?

Contributors have made commits to the specified repositories/organization on a default branch. Contributions can also be issue, pull request and discussion interactions. The endpoint used may return information that is a few hours old because the GitHub REST API caches contributor data to improve performance.

GitHub identifies contributors by author email address. Contribution counts are grouped by GitHub user, which includes all associated email addresses. To improve performance, only the first 500 author email addresses in the repository link to GitHub users. The rest will appear as anonymous contributors without associated GitHub user information.

Find out more in the [GitHub API documentation](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-contributors).

## Use as a GitHub Action

1. Create a repository to host this GitHub Action or select an existing repository.
1. Select a best fit workflow file from the [examples below](#example-workflows).
1. Copy that example into your repository (from step 1) and into the proper directory for GitHub Actions: `.github/workflows/` directory with the file extension `.yml` (ie. `.github/workflows/contributors.yml`)
1. Edit the values below from the sample workflow with your information:
   - `ORGANIZATION`
   - `REPOSITORY`
   - `START_DATE`
   - `END_DATE`

   If no **start and end date** are supplied, the action will consider the entire repository history and be unable to determine if contributors are new or returning.
   If running on a whole **organization** then no repository is needed.  
   If running the action on just **one repository** or a **list of repositories**, then no organization is needed.

1. Also edit the value for `GH_ENTERPRISE_URL` if you are using a GitHub Server and not using github.com.  
   For github.com users, leave it empty.
1. If you are running this action on an organization or repository other than the one where the workflow file is going to be, then update the value of `GH_TOKEN`.
   - Do this by creating a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) with permissions to read the repository/organization and write issues.
   - Then take the value of the API token you just created, and [create a repository secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) where the name of the secret is `GH_TOKEN` and the value of the secret the API token.
   - Then finally update the workflow file to use that repository secret by changing `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to `GH_TOKEN: ${{ secrets.GH_TOKEN }}`. The name of the secret can really be anything. It just needs to match between when you create the secret name and when you refer to it in the workflow file.
1. If you want the resulting issue with the output to appear in a different repository other than the one the workflow file runs in, update the line `token: ${{ secrets.GITHUB_TOKEN }}` with your own GitHub API token stored as a repository secret.
   - This process is the same as described in the step above. More info on [creating secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) can be found.
1. Commit the workflow file to the default branch (often `master` or `main`)
1. Wait for the action to trigger based on the `schedule` entry or manually trigger the workflow as shown in the [documentation](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow).

### Configuration

Below are the allowed configuration options:

#### Authentication

This action can be configured to authenticate with GitHub App Installation or Personal Access Token (PAT). If all configuration options are provided, the GitHub App Installation configuration has precedence. You can choose one of the following methods to authenticate:

##### GitHub App Installation

| field                        | required | default | description                                                                                                                                                                                             |
| ---------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GH_APP_ID`                  | True     | `""`    | GitHub Application ID. See [documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app) for more details.              |
| `GH_APP_INSTALLATION_ID`     | True     | `""`    | GitHub Application Installation ID. See [documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app) for more details. |
| `GH_APP_PRIVATE_KEY`         | True     | `""`    | GitHub Application Private Key. See [documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app) for more details.     |
| `GITHUB_APP_ENTERPRISE_ONLY` | False    | false   | Set this input to `true` if your app is created in GHE and communicates with GHE.                                                                                                                       |

##### Personal Access Token (PAT)

| field      | required | default | description                                                                                                           |
| ---------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| `GH_TOKEN` | True     | `""`    | The GitHub Token used to scan the repository. Must have read access to all repository you are interested in scanning. |

#### Other Configuration Options

| field               | required                                        | default           | description                                                                                                                                                                                                              |
| ------------------- | ----------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GH_ENTERPRISE_URL` | False                                           | ""                | The `GH_ENTERPRISE_URL` is used to connect to an enterprise server instance of GitHub. github.com users should not enter anything here.                                                                                  |
| `ORGANIZATION`      | Required to have `ORGANIZATION` or `REPOSITORY` |                   | The name of the GitHub organization which you want the contributor information of all repos from. ie. github.com/github would be `github`                                                                                |
| `REPOSITORY`        | Required to have `ORGANIZATION` or `REPOSITORY` |                   | The name of the repository and organization which you want the contributor information from. ie. `github/contributors` or a comma separated list of multiple repositories `github/contributor,super-linter/super-linter` |
| `START_DATE`        | False                                           | Beginning of time | The date from which you want to start gathering contributor information. ie. Aug 1st, 2023 would be `2023-08-01`.                                                                                                        |
| `END_DATE`          | False                                           | Current Date      | The date at which you want to stop gathering contributor information. Must be later than the `START_DATE`. ie. Aug 2nd, 2023 would be `2023-08-02`                                                                       |
| `SPONSOR_INFO`      | False                                           | False             | If you want to include sponsor information in the output. This will include the sponsor count and the sponsor URL. This will impact action performance. ie. SPONSOR_INFO = "False" or SPONSOR_INFO = "True"              |
| `LINK_TO_PROFILE`   | False                                           | True              | If you want to link usernames to their GitHub profiles in the output. ie. LINK_TO_PROFILE = "True" or LINK_TO_PROFILE = "False"                                                                                          |
| `OUTPUT_FILENAME`   | False                                           | contributors.md   | The output filename for the markdown report. ie. OUTPUT_FILENAME = "my-report.md"                                                                                                                                        |
| `SHOW_AVATAR`       | False                                           | False             | If you want to show profile images in the markdown output. ie. SHOW_AVATAR = "True" or SHOW_AVATAR = "False"                                                                                                             |

**Note**: If `start_date` and `end_date` are specified then the action will determine if the contributor is new. A new contributor is one that has contributed in the date range specified but not before the start date.

**Performance Note:** Using start and end dates will reduce speed of the action by approximately 63X. ie without dates if the action takes 1.7 seconds, it will take 1 minute and 47 seconds.

### Example workflows

**Be sure to change at least these values: `<YOUR_ORGANIZATION_GOES_HERE>`, `<YOUR_GITHUB_HANDLE_HERE>`**

```yaml
name: Monthly contributor report
on:
  workflow_dispatch:
  schedule:
    - cron: "3 2 1 * *"

permissions:
  contents: read

jobs:
  contributor_report:
    name: contributor report
    runs-on: ubuntu-latest
    permissions:
      issues: write
    env:
      OUTPUT_FILENAME: contributors.md

    steps:
      - name: Get dates for last month
        shell: bash
        run: |
          # Calculate the first day of the previous month
          start_date=$(date -d "last month" +%Y-%m-01)

          # Calculate the last day of the previous month
          end_date=$(date -d "$start_date +1 month -1 day" +%Y-%m-%d)

          #Set an environment variable with the date range
          echo "START_DATE=$start_date" >> "$GITHUB_ENV"
          echo "END_DATE=$end_date" >> "$GITHUB_ENV"

      - name: Run contributor action
        uses: github-community-projects/contributors@v2
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          START_DATE: ${{ env.START_DATE }}
          END_DATE: ${{ env.END_DATE }}
          ORGANIZATION: <YOUR_ORGANIZATION_GOES_HERE>
          SPONSOR_INFO: "true"

      - name: Create issue
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: Monthly contributor report
          token: ${{ secrets.GITHUB_TOKEN }}
          content-filepath: ./${{ env.OUTPUT_FILENAME }}
          assignees: <YOUR_GITHUB_HANDLE_HERE>
```

#### Using GitHub app

```yaml
name: Monthly contributor report
on:
  workflow_dispatch:
  schedule:
    - cron: "3 2 1 * *"

permissions:
  contents: read

jobs:
  contributor_report:
    name: contributor report
    runs-on: ubuntu-latest
    permissions:
      issues: write
    env:
      OUTPUT_FILENAME: contributors.md

    steps:
      - name: Get dates for last month
        shell: bash
        run: |
          # Calculate the first day of the previous month
          start_date=$(date -d "last month" +%Y-%m-01)

          # Calculate the last day of the previous month
          end_date=$(date -d "$start_date +1 month -1 day" +%Y-%m-%d)

          #Set an environment variable with the date range
          echo "START_DATE=$start_date" >> "$GITHUB_ENV"
          echo "END_DATE=$end_date" >> "$GITHUB_ENV"

      - name: Run contributor action
        uses: github-community-projects/contributors@v2
        env:
          GH_APP_ID: ${{ secrets.GH_APP_ID }}
          GH_APP_INSTALLATION_ID: ${{ secrets.GH_APP_INSTALLATION_ID }}
          GH_APP_PRIVATE_KEY: ${{ secrets.GH_APP_PRIVATE_KEY }}
          # GITHUB_APP_ENTERPRISE_ONLY: True --> Set to true when created GHE App needs to communicate with GHE api
          GH_ENTERPRISE_URL: ${{ github.server_url }}
          # GH_TOKEN: ${{ steps.app-token.outputs.token }} --> the token input is not used if the github app inputs are set
          START_DATE: ${{ env.START_DATE }}
          END_DATE: ${{ env.END_DATE }}
          ORGANIZATION: <YOUR_ORGANIZATION_GOES_HERE>
          SPONSOR_INFO: "true"

      - name: Create issue
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: Monthly contributor report
          token: ${{ secrets.GITHUB_TOKEN }}
          content-filepath: ./${{ env.OUTPUT_FILENAME }}
          assignees: <YOUR_GITHUB_HANDLE_HERE>
```

## Example Markdown output with `start_date` and `end_date` supplied

```markdown
# Contributors

- Date range for contributor list: 2021-01-01 to 2023-10-10
- Organization: super-linter

| Total Contributors | Total Contributions | % new contributors |
| ------------------ | ------------------- | ------------------ |
| 1                  | 143                 | 0%                 |

| Username  | All Time Contribution Count | New Contributor | Commits between 2021-01-01 and 2023-10-10                                                                                           |
| --------- | --------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| @zkoppert | 143                         | False           | [super-linter/super-linter](https://github.com/super-linter/super-linter/commits?author=zkoppert&since=2021-01-01&until=2023-10-10) |
```

## Example Markdown output with no dates supplied

```markdown
#### Contributors

- Organization: super-linter

| Total Contributors | Total Contributions | % new contributors |
| ------------------ | ------------------- | ------------------ |
| 1                  | 1913                | 0%                 |

| Username  | All Time Contribution Count | New Contributor | Sponsor URL                                          | Commits between 2021-09-01 and 2023-09-30                                                                                           |
| --------- | --------------------------- | --------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| @zkoppert | 1913                        | False           | [Sponsor Link](https://github.com/sponsors/zkoppert) | [super-linter/super-linter](https://github.com/super-linter/super-linter/commits?author=zkoppert&since=2021-09-01&until=2023-09-30) |
```

## GitHub Actions Job Summary

When running as a GitHub Action, the contributors report is automatically displayed in the [GitHub Actions Job Summary](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary). This provides immediate visibility of the results directly in the workflow run interface without needing to check separate files or issues.

The job summary contains the same markdown content that is written to the configured output file (`contributors.md` by default), making it easy to view contributor information right in the GitHub Actions UI.

## Local usage without Docker

1. Make sure you have at least Python3.11 installed
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. Copy `.env-example` to `.env`
1. Fill out the `.env` file with a _token_ from a user that has access to the organization to scan (listed below). Tokens should have at least read:org access for organization scanning and read:repository for repository scanning.
1. Fill out the `.env` file with the configuration parameters you want to use
1. `uv sync`
1. Run `uv run python3 ./contributors.py`, which will output everything in the terminal

## License

[MIT](LICENSE)

## More OSPO Tools

Looking for more resources for your open source program office (OSPO)? Check out the [`github-ospo`](https://github.com/github/github-ospo) repo for a variety of tools designed to support your needs.
