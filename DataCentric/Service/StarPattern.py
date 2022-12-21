import re
class StarPattern:
    def __init__(self,workload):
        self.workload=workload
        self.prefix=self.find_prefix()
        self.stars,self.connectors=self.find_stars()

    
    # private functions
    def find_stars(self):
        file=open(self.workload,"r")
        stars={}
        star_properties={}
        star_connectors=[]
        query_stars=[]
        objects=[]
        query_counter=0
        for line in file.readlines():
            if "{" in line:
                query_counter+=1
                continue
            elif ":" in line and "#" not in line and line.startswith("PREFIX")==False:

                patterns=line.replace("\t","").split(" ")
                subject=patterns[0]
                property=patterns[1]
                
                property_key=property.split(":")[0]+":"
            
                if property_key in self.prefix:
                    
                    property=property.replace(property_key,self.prefix[property_key])

                if property=="http___www_w3_org_1999_02_22_rdf_syntax_ns_type":
                    continue

                object=patterns[2]
                
                if subject not in query_stars:
                    query_stars.append(subject)
                
                if "?" in object or "http://" in object:
                    objects.append((object,property))
                
                if subject not in star_properties:
                    star_properties[subject]=[property]
                else:
                    my_list=star_properties[subject]
                    my_list.append(property)
                    star_properties[subject]=my_list

            elif "}" in line:
                stars["query"+str(query_counter)]=star_properties
                for object in objects:
                    if object[0] in star_properties:
                        star_connectors.append(object[1])

                star_properties={}
                objects=[]
            
        return (stars,set(star_connectors))
                    
    def combine_stars(self):

        stars_dict={}
        counter=0
        for key,value in self.stars.items():
            for k,v in value.items():
                is_combined=False
                if len(stars_dict)==0:
                    stars_dict["star"+str(counter)]=v
                    counter+=1
                    is_combined=True
                else:
                    for k1,v1 in stars_dict.items():
                        if len(list(set(v).intersection(set(v1))))!=0:
                            # print("Joined:",v)
                            # print("Combined:",v1)
                            union=list(set(v).union(set(v1)))
                            # print("Union:",union)
                            stars_dict[k1]=union
                            is_combined=True
                            # print("------------------------")

                
                if is_combined==False:
                    counter+=1
                    stars_dict["star"+str(counter)]=v


        for k,v in stars_dict.items():
            for k1,v1 in stars_dict.items():
                if k!=k1 and len(list(set(v).intersection(v1)))!=0:
                    union=list(set(v).union(v1))
                    stars_dict[k1]=union
                    stars_dict[k]=()           

        return stars_dict

    def find_prefix(self):
        prefix={}
        file=open(self.workload,"r")

        for line in file.readlines():
            if line.startswith("PREFIX"):
                group=line.split(" ")[1]
                url=line.split(" ")[2].replace("<","").replace(">","").replace(" ","")
                prefix[group]="".join([ c if c.isalnum() else "_" for c in url])[:-1]
                
        return prefix