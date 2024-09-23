# github-pull-request-metrics
Scripts to extract metrics from Pull Requests

# 1. PR Size
Description: This metric measures the number of lines of code (LOC) changed in the Pull Request, including lines added, removed, or modified. The number of affected files may also be considered.

## Expectations:

PRs are recommended to be small and manageable to facilitate code review and reduce complexity. PRs that are too large are often harder to review and more likely to introduce bugs.
An optimal PR size could be between 200-400 lines of code, but will depend on the team and project.
Common indicators:

Large PRs: May indicate division of labor issues or development practices that hinder collaboration (it is better to break large PRs into smaller PRs).
Small PRs: Often correlate with faster feedback cycles and better code review.

#2. PR Request Cycle Time
Description: Cycle time measures the total time from when a PR is opened until it is closed (either because it is merged, rejected, or closed for any other reason).

## Expectations:

A short cycle time is ideal, as it implies that changes move quickly from request to integration. Cycle time depends on code review, requested fixes, and final approval.
Expectations could be 1-3 days depending on team size and workload.
Common indicators:

Long cycle times: Can point to issues such as long review queues, reliance on busy reviewers, or overly large and complex PRs.
Short cycle times: Reflect an agile team with good review practices and a culture of rapid feedback.

# 3. PR Code Review Lead Time
Description: This is the time it takes from when a PR is ready for review until a reviewer begins the review. It measures the efficiency of reviewers.

## Expectations:

Ideally, reviewers should respond and begin reviewing a PR quickly. A good goal might be less than 24 hours on active development teams.
Common indicators:

Long review times: Can mean that reviewers are overloaded or that there is poor assignment of responsibilities.
Short review times: Indicate that reviewers are available and active, which improves fast feedback and workflow.

# 4. PR Success Rate
Description: This metric measures the percentage of PRs that are accepted and merged into the codebase versus those that are rejected, abandoned, or require major changes.

What to expect:

A high success rate means that developers are delivering high-quality PRs, making it easy to approve them without many edits.
Ideally, you'd want a success rate of 80-90% or higher, but it will depend on the team and context.
Common indicators:

Low success rate: This can indicate problems with requirements, lack of clarity in reviews, or that PRs are being submitted before they are fully ready.
High success rate: This means that there is good communication, PRs are well prepared, and changes are generally accepted without major conflicts.

# 5. PR Comments Count
Description: This measures the number of comments that are made on a PR, both by reviewers and authors.

## What to expect:

A moderate number of comments indicates that reviewers are actively participating, providing valuable feedback. This is positive if the comments are constructive and help improve the quality of the code.
If there are too many comments, it may signal that the PR is too complex or that the code requires a lot of fixes.
Common indicators:

Too few comments: It could indicate a lack of feedback from reviewers or that the PRs are trivial.
Too many comments: It may indicate that the PR has too many areas for improvement or that reviewers are finding too many issues, which could suggest the need to split the PR or improve quality before review.

# Summary:
PR Size: Small and manageable is ideal.
PR Request Cycle Time: Short, 1-3 days.
PR Code Review Lead Time: Fast, less than 24 hours.
PR Success Rate: High, 80-90% or more.
PR Comments Count: Moderate, enough to improve the code without overloading it.
