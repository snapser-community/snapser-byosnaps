# !/bin/bash
snapctl validate
snapctl byosnap publish --byosnap-id byosnap-python-basic --version "v1.0.0" --resources-path `pwd`/resources --path `pwd`
