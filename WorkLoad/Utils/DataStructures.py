import numpy as np
from Service.Parser import Parser

class DataStructures:
    def __init__(self,QuerySets) -> None:
        self.QuerySets=QuerySets
        
        self.all_columns="s,http___purl_org_goodrelations_offers,http___schema_org_wordCount,http___xmlns_com_foaf_homepage,http___purl_org_ontology_mo_producer,http___schema_org_actor,http___schema_org_numberOfPages,http___purl_org_ontology_mo_movement,http___schema_org_birthDate,http___db_uwaterloo_ca__galuc_wsdbm_purchaseDate,http___schema_org_producer,http___purl_org_stuff_rev_hasReview,http___schema_org_isbn,http___purl_org_ontology_mo_performer,http___purl_org_goodrelations_name,http___schema_org_director,http___purl_org_ontology_mo_record_number,http___schema_org_jobTitle,http___schema_org_openingHours,http___schema_org_language,http___schema_org_publisher,http___purl_org_dc_terms_Location,http___www_geonames_org_ontology_parentCountry,http___schema_org_aggregateRating,http___www_w3_org_1999_02_22_rdf_syntax_ns_type,http___schema_org_employee,http___purl_org_goodrelations_price,http___schema_org_award,http___schema_org_duration,http___purl_org_goodrelations_description,http___schema_org_faxNumber,http___schema_org_expires,http___schema_org_eligibleQuantity,http___purl_org_stuff_rev_title,http___db_uwaterloo_ca__galuc_wsdbm_composer,http___db_uwaterloo_ca__galuc_wsdbm_gender,http___ogp_me_ns_title,http___schema_org_editor,http___purl_org_stuff_rev_rating,http___purl_org_goodrelations_includes,http___db_uwaterloo_ca__galuc_wsdbm_hits,http___schema_org_trailer,http___schema_org_keywords,http___purl_org_goodrelations_validThrough,http___schema_org_email,http___schema_org_priceValidUntil,http___purl_org_ontology_mo_performed_in,http___schema_org_nationality,http___purl_org_stuff_rev_reviewer,http___schema_org_text,http___db_uwaterloo_ca__galuc_wsdbm_makesPurchase,http___schema_org_description,http___schema_org_bookEdition,http___db_uwaterloo_ca__galuc_wsdbm_userId,http___purl_org_ontology_mo_opus,http___schema_org_telephone,http___schema_org_contentSize,http___xmlns_com_foaf_familyName,http___purl_org_goodrelations_serialNumber,http___purl_org_ontology_mo_release,http___schema_org_datePublished,http___purl_org_stuff_rev_totalVotes,http___db_uwaterloo_ca__galuc_wsdbm_hasGenre,http___schema_org_printPage,http___purl_org_stuff_rev_text,http___purl_org_ontology_mo_conductor,http___ogp_me_ns_tag,http___schema_org_eligibleRegion,http___xmlns_com_foaf_givenName,http___db_uwaterloo_ca__galuc_wsdbm_follows,http___schema_org_paymentAccepted,http___xmlns_com_foaf_age,http___purl_org_ontology_mo_artist,http___schema_org_printSection,http___schema_org_author,http___purl_org_goodrelations_validFrom,http___schema_org_printColumn,http___schema_org_caption,http___schema_org_url,http___db_uwaterloo_ca__galuc_wsdbm_likes,http___schema_org_contentRating,http___schema_org_printEdition,http___db_uwaterloo_ca__galuc_wsdbm_purchaseFor,http___schema_org_legalName,http___db_uwaterloo_ca__galuc_wsdbm_subscribes,http___db_uwaterloo_ca__galuc_wsdbm_friendOf,http___schema_org_contactPoint".split(',') # here will calculate all distinct attributes
        print(len(self.all_columns))
        self.usage_matrix=self.generate_attribute_usage_matrix(self.QuerySets)
        self.affinity_matrix=self.generate_attribute_affinity_matrix(self.usage_matrix)
    
    #---- private functions -----

    def generate_attribute_usage_matrix(self,columns):
        attribute_usage_matrix=[]
        for column in columns:
            
            query_matrix=[]

            for element in self.all_columns:
                for item in column:
                    if item in element:
                        query_matrix.append(1)
                    else:
                        query_matrix.append(0)

            attribute_usage_matrix.append(query_matrix)
        
        return attribute_usage_matrix
    
    def generate_attribute_affinity_matrix(self,usage_matrix):

        n_attributes=len(self.all_columns)
        n_queries=len(self.QuerySets)
        
        affinity_matrix=np.zeros((n_attributes,n_attributes))

        for i in range(n_attributes):
            for j in range(n_attributes):
                for q in range(n_queries):
                    if usage_matrix[q][i]==1 and usage_matrix[q][j]==1:
                        affinity_matrix[i][j]= affinity_matrix[i][j]+1

        return affinity_matrix
    
    def dot_prod(self,vec_a, vec_b):
        return np.dot(vec_a.flatten(), vec_b.flatten())

    def BEA(self,aa_matrix):
        cc_matrix = aa_matrix[:, :2]
        cc_matrix = np.append(np.zeros((len(self.all_columns),1)), cc_matrix, axis=1)
        cc_matrix = np.append(cc_matrix,np.zeros((len(self.all_columns),1)), axis=1)

        # BOND ENERGY ALGORITHM - CC_MATRIX GENERATION
        for k in range(2, len(aa_matrix)):
            i, j = 0, 1
            get_values = []
            while j < cc_matrix.shape[1]:
                print(i,k,j, len(cc_matrix))
                get_values.append(2 * self.dot_prod(cc_matrix[:, i:i+1], aa_matrix[:, k:k+1]) + 
                                2 * self.dot_prod(aa_matrix[:, k:k+1], cc_matrix[:, j:j+1]) - 
                                2 * self.dot_prod(cc_matrix[:, i:i+1], cc_matrix[:, j:j+1]))  
                i = j
                j+=1
        pos = np.argmax(get_values) + 1
        cc_matrix = np.insert(cc_matrix, pos, aa_matrix[k:k+1], axis=1)

        # BOND ENERGY ALGORITHM - REMOVES ZEROS COLUMNS
        cc_matrix = np.delete(cc_matrix, 0, axis=1)
        cc_matrix = np.delete(cc_matrix, cc_matrix.shape[1]-1, axis=1)

        return cc_matrix
    


    #--- end of private functions -----
    