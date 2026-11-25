# What earns a developer’s attention?

**Decision, 25 November 2026.** Build a rehearsal around one change an engineer already understands. A candidate can practice explaining a decision, a teammate can use the same questions in a review, and a mentor can ask for a counterexample. The public demo should let all three try it before installing anything.

## Two samples and a denominator

At approximately 09:40 UTC we queried GitHub Repository Search, sorted by descending stars, excluded forks and saved the first 30 results for each query. The all-time query used `stars:>10000 is:public fork:false`. The recent query used `created:2026-10-25..2026-11-23 is:public fork:false stars:>0`. The recent sample spans 30 calendar days and gives older entries more time to accumulate stars. Both searches reported complete results. Rankings and counts can change after collection. [60 source-linked observations](repositories.csv) · [Repository search API](https://docs.github.com/en/rest/search/search#search-repositories)

| Selected observation | Stars at collection | Product decision it informed |
| --- | ---: | --- |
| [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) | 565,395 | Give the reader something to do immediately. |
| [System Design Primer](https://github.com/donnemartin/system-design-primer) | 379,149 | Use questions about alternatives and their costs. |
| [Coding Interview University](https://github.com/jwasham/coding-interview-university) | 365,024 | Let an engineer practice independently and return later. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 332,506 | Package the interview method separately so an agent can run it. |
| [unslop](https://github.com/heydamir/unslop) | 21,434 | Show the output of one narrowly defined skill in the README. |
| [floorplan](https://github.com/haydenschmitty/floorplan) | 6,756 | Make a developer’s own checkout the input to an explanatory artifact. |

Six of the all-time top ten explicitly teach programming, engineering or interview preparation in their description. They include Build Your Own X, freeCodeCamp, Free Programming Books, System Design Primer, Developer Roadmap and Coding Interview University. Among the recent top ten are a focused UI skill, a collection of agent skills, a download manager and a container runtime. These are several different paths to attention. Counting only winners hides how rarely any new repository reaches those numbers.

We repeated the recent-window search using four star thresholds and retained the API’s aggregate counts. Each returned `incomplete_results=false`. Zero-star and positive-star queries together returned **9,648,640** repositories.

| Stars at collection | Matching repositories | Share of the window |
| --- | ---: | ---: |
| 0 | 9,192,361 | 95.27% |
| 1 or more | 456,279 | 4.73% |
| 100 or more | 3,564 | 0.037% |
| 1,000 or more | 179 | 0.0019% |

The threshold rows overlap. This denominator includes personal exercises, mirrors and unpromoted repositories. It describes public repository creation, and cannot supply a launch probability for a finished developer tool. We did not observe first-ten-hour star histories or repository traffic for these cohorts.

## Why people save a project

In a survey of 791 respondents, 52.5% cited appreciation and 51.1% cited bookmarking as reasons for starring a specific repository. Respondents could give multiple reasons. A workbook a developer might revisit before a review fits that bookmarking use case. Whether people will actually return requires observation. [Borges and Valente, *What’s in a GitHub Star?*](https://arxiv.org/abs/1811.07643)

Julia Evans describes reconstructing months of engineering work from pull requests, tickets, design docs and emails before reviews. Commits are a practical starting point for recall. They leave out mentorship, coordination and production outcomes. That is why the last prompt asks the engineer for their role and an observed result. [Get your work recognized](https://jvns.ca/blog/brag-documents/)

## Comparable tools

| Project | What the maintainer offers | Why choose Diff Rehearsal for a session? |
| --- | --- | --- |
| [Open Interview](https://github.com/yeyimilk/open-interview) | A self-hosted mentor grounded in a project and resume, with an LLM key or local model | Generate one browser file from a checkout using Python and Git. |
| [Interview My Project](https://github.com/WarlCang/interview-my-project) | An agent interviews you about your project and can use local agent transcripts | Practice one revision. The generator reads commit metadata and file statistics. |
| [brag-cli](https://github.com/eduardohitek/brag-cli) | Tracks achievements, syncs work items and generates performance reports | Rehearse the reasoning behind a single engineering change in four questions. |

The two directly comparable interview projects had 9 and 14 stars at collection. That is a stronger caution about this niche than the lifetime popularity of interview curricula. We chose a downloadable, model-free workbook as a testable distinction. A general interview-question collection would enter a category with established curricula. A full project interviewer would reproduce capabilities that already exist.

## What the first ten hours can tell us

EmbedPDF’s author reported over 500 stars in 24 hours after a single successful Show HN post. The author of breakscale reported six stars in 13.5 hours after a post with 54,783 views, then much faster growth after a demonstration circulated. Those are selected, self-reported launches, with different audiences and distribution. Their numbers distinguish reach from conversion and illustrate how little a push alone predicts. [EmbedPDF launch account](https://dev.to/bobsingor/how-i-got-500-stars-in-24-hours-on-my-first-public-github-repo-1afg) · [breakscale hour-by-hour account](https://launchmaxxing.co/guides/first-1000-github-stars)

Record the push time and public star/fork counts at launch, +5 h and +10 h. Use a release asset’s download count as a rough sign of trials. Downloads include repeats and automation. GitHub’s Traffic view provides unique visitors and cloners over a rolling 14-day window and may update later. A social platform’s impression count comes from that platform. Without it, impressions remain unknown. None of these counters establishes that someone finished a workbook. A feedback report naming a confusing question or a productive follow-up is stronger evidence of use. [GitHub traffic documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository)
