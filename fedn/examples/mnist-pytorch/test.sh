#!/usr/bin/env zsh

# Load zsh/mathfunc module for floating-point support
autoload -Uz zmathfunc
zmodload zsh/mathfunc

# Define the ratio
mal_ratio=80

# Calculate the fraction
fraction=$(echo "$mal_ratio / 100" | bc -l)

# Print the fraction
echo $fraction
