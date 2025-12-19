"""Generate the distributions codebook PDF for the tutorial."""

import numpy as np
from bookit_df import BookIt

# Set seed for reproducibility  
np.random.seed(42)
n = 1000  # Number of observations per distribution

# Normal distribution: μ=0, σ=1
normal_data = np.random.normal(loc=0, scale=1, size=n)

# Exponential distribution: λ=1.5
exponential_data = np.random.exponential(scale=1/1.5, size=n)

# Uniform distribution: a=0, b=10
uniform_data = np.random.uniform(low=0, high=10, size=n)

# Poisson distribution: λ=5
poisson_data = np.random.poisson(lam=5, size=n)

# Binomial distribution: n=20, p=0.3
binomial_data = np.random.binomial(n=20, p=0.3, size=n)

# Beta distribution: α=2, β=5
beta_data = np.random.beta(a=2, b=5, size=n)

# Gamma distribution: k=2, θ=2
gamma_data = np.random.gamma(shape=2, scale=2, size=n)

with BookIt(
    "Probability Distributions Codebook",
    output="docs/assets/distributions_codebook.pdf",
    author="Data Science Team"
) as book:
    
    # Normal distribution
    book.add_variable(
        name="normal",
        description="Standard normal distribution",
        context="Parameters: μ (mean) = 0, σ (std dev) = 1. "
                "The normal distribution is symmetric and bell-shaped, "
                "commonly used to model natural phenomena.",
        data=normal_data
    )
    
    # Exponential distribution
    book.add_variable(
        name="exponential",
        description="Exponential distribution",
        context="Parameters: λ (rate) = 1.5. "
                "Models time between events in a Poisson process. "
                "Commonly used for survival analysis and reliability engineering.",
        data=exponential_data
    )
    
    # Uniform distribution
    book.add_variable(
        name="uniform",
        description="Continuous uniform distribution",
        context="Parameters: a (min) = 0, b (max) = 10. "
                "Every value in the interval has equal probability. "
                "Used for random sampling and Monte Carlo simulations.",
        data=uniform_data
    )
    
    # Poisson distribution
    book.add_variable(
        name="poisson",
        description="Poisson distribution",
        context="Parameters: λ (rate) = 5. "
                "Models count of events in a fixed interval. "
                "Common in queueing theory and epidemiology.",
        data=poisson_data
    )
    
    # Binomial distribution
    book.add_variable(
        name="binomial",
        description="Binomial distribution",
        context="Parameters: n (trials) = 20, p (success probability) = 0.3. "
                "Models number of successes in a fixed number of trials. "
                "Used in quality control and clinical trials.",
        data=binomial_data
    )
    
    # Beta distribution
    book.add_variable(
        name="beta",
        description="Beta distribution",
        context="Parameters: α (shape) = 2, β (shape) = 5. "
                "Bounded between 0 and 1, useful for modeling proportions. "
                "Common as a prior in Bayesian statistics.",
        data=beta_data
    )
    
    # Gamma distribution
    book.add_variable(
        name="gamma",
        description="Gamma distribution",
        context="Parameters: k (shape) = 2, θ (scale) = 2. "
                "Generalizes the exponential distribution. "
                "Used to model waiting times and insurance claims.",
        data=gamma_data
    )

print("Generated: docs/assets/distributions_codebook.pdf")
