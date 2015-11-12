#!/usr/bin/python
#################################################################################
#--------------------------------Usage Sample-----------------------------------#
#################################################################################
from retailor import * 

r=Retailor("./the")
(
    r.use(yaml_frontmatter)
     .use(meta_dir,"posts","render")
     .use(meta_dir,"posts","post")
     .use(jinja2,{
         'posts': r.ls("post"),
         'fronts': r.ls("front")

     })
     .use(save,"./other")
     .do()
)
