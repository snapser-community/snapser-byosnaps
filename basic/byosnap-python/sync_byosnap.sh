# !/bin/bash
snapctl validate
snapctl byosnap sync --snapend-id hihd45xb --byosnap-id byosnap-python-basic --version "v1.0.0" --resources-path `pwd`/resources --path `pwd`

