#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cma

es = cma.CMAEvolutionStrategy(8 * [0], 0.5)

es.optimize(cma.ff.rosen)

# Pretty print result
es.result_pretty()
