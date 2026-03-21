# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
I used the **Bureau of Transportation Statistics (BTS) On-Time Reporting** dataset for January 2025. This CSV includes flight data for all domestic operations by major U.S. air carriers, specifically capturing scheduled vs. actual departure times and cancellation status.  Further refinement would be needed for comprehensive analysis (i.e. including time made back up enroute to the destination, delay reasons outside the airline's control, etc.), but to demonstrate understanding of the concepts of this assignment it only looked at delays on departure vs scheduled times.

### Signals
I created a **High Delay Alert** signal based on a **20% threshold**. A flight was marked as "delayed" if it departed **15 minutes or more** past its scheduled time or if the flight was **cancelled**. The signal applies a boolean `true/false` flag to each carrier to identify those struggling with operational punctuality.

### Experiments
I modified the original Polars-based signal recipe to aggregate raw flight data by the `OP_UNIQUE_CARRIER` column. I experimented with identifying "problematic" performance by calculating the ratio of delayed/cancelled flights against total flight volume (`flights`), ensuring that the logic captured both flights that departed late and not at all.

### Results
The analysis processed 14 major carriers. With a 20% alert threshold, the results show:

| Carrier        | Flights | Delayed | Delay Rate | High Delay Alert |
|----------------|---------|---------|------------|------------------|
| WN (Southwest) | 105307  | 20891   | 19.8%      | false            |
| UA (United)    | 62007   | 11299   | 18.2%      | false            |
| AS (Alaska)    | 18163   | 3236    | 17.8%      | false            |
| YX (Republic)  | 27833   | 4392    | 15.8%      | false            |
| HA (Hawaiian)  | 6690    | 874     | 13.1%      | false            |
| MQ (Envoy)     | 21890   | 4314    | 19.7%      | false            |
| F9 (Frontier)  | 15526   | 3903    | 25.1%      | true             |
| OO (SkyWest)   | 65036   | 13253   | 20.4%      | true             |
| DL (Delta)     | 76306   | 16661   | 21.8%      | true             |
| B6 (JetBlue)   | 17918   | 4264    | 23.8%      | true             |
| OH (PSA)       | 21094   | 6338    | 30.0%      | true             |
| NK (Spirit)    | 17544   | 3656    | 20.8%      | true             |
| G4 (Allegiant) | 9345    | 2294    | 24.5%      | true             |
| AA (American)  | 75088   | 16369   | 21.8%      | true             |

### Interpretation
This analysis provides critical business intelligence by normalizing performance across carriers of different sizes. While Southwest had the highest volume of total flights, its ability to stay under the 20% threshold suggests higher operational resilience compared to Delta, which triggered the "High Delay Alert." For an aviation system, this signal serves as an early warning for staffing or resource allocation issues within specific carrier networks.
