#!/bin/bash

atlas deployments search indexes create --file indexDef-vector.json
atlas deployments search indexes create --file indexDef-vector-cosine.json