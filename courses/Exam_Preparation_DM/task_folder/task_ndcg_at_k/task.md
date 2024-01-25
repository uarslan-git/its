# nDCG

Consider a recommendation list $$r \in \mathbb{N}^n$$ where entries $$r_i$$ represent the relevance of item $$i$$ to the user. Normalized Discounted Cumulative Gain (nDCG) is a metric used to evaluate the ranking quality of a recommendation list. 
Among others, this is a metric very commonly used to evaluate the quality of a recommender system. 
In this task, please write a function for computing the nDCG of a recommendation list @k: that is, you only have to evaluate the quality of the recommendations on the first k positions in the list.