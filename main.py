'''
- Prepare cognitive schematics to work on.
- Implement functions : Deduction :
    - Estimate the context truth for each schematics(check if the current schema's contexts hold true in the current percepta record )
    - Filter For the valid schematics : only those contexts that are currently valid are chosen.
- Build the Mixture Model
    - For each valid schematic, we extract the action, then compute the weights for the schematics . 
        - The weight is calculated as : weight = prior_probability * beta_factor
                where :
                    prior_probability = exp(-complexity_penality * penality)
                        complexity_penality : is a tunable penality variable.
                        complexity : the number of unique atonms in the schematics. 
                    beta_factor : this quantifies the statistical evidence from the observed successes and failures(I need to have more detailed information on this one)

    - After we calculate the weights for each schematics , we now have  a list of pairs of CogSchematics-weight
        - in addition to that , we add a small number delta to the weight in order to guarantee that atleast one action is selected. (its basically like having a fallback when there is no matching schematics)
    - Group schematics by the actions they support.
        - we can accumulate their weights (need more info on this as well)
    - Then for each action :
        - We randomly select one schematics (usually the one with the highest weight, but the rest of the schematics also have the chance to be selected)
        - For the selected schematics we sample the probability of success from its beta destribution.
        - Adjust the sampled probability by the schematics' weight.[optional]
    
- Thompson Sampling : to select the best action.

'''
