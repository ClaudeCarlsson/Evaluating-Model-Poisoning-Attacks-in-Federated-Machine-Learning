#!/bin/bash

# Navigate to Gradient_Attack and build image
cd Gradient_Attack
docker build . -t grad-fedn-client
cd ..

# Navigate to Gradient_Inv_Attack and build image
cd Gradient_Inv_Attack
docker build . -t grad-inv-fedn-client
cd ..

