from pyspark.sql import SparkSession
from pyspark.sql.functions import round
from pyspark.sql.functions import lit
from pyspark.sql.functions import col, when
from pyspark.sql.functions import col, when


def prime_assurance(file_csv):

    # colonnes à retenir dans file_csv  : ID, age, gender, driving_experience, education, income, vehicule_ownership, vehicule_year, postal_code, past_accidents, outcome, speeding_violations

    new_df_1 = file_csv.drop("RACE","CREDIT_SCORE","MARRIED","CHILDREN")
    new_df_1.show(5)

    distinct_values = new_df_1.select("VEHICLE_TYPE").distinct().collect()
    for value in distinct_values:
        print(value[0])

    # Création des colonnes insurance_premium, base_premium, risk_coefficient
    
    new_df_1 = new_df_1.withColumn("base_premium", lit(0.0))
    new_df_1 = new_df_1.withColumn("risk_coefficient", lit(0.0))
    new_df_1 = new_df_1.withColumn("insurance_premium", lit(0.0))

    # Calcul de la base premium 
    

    new_df_1 = new_df_1.withColumn("base_premium",
                                when((col("VEHICLE_TYPE") == "Sports Car"), 1000)
                                .otherwise(700))

    new_df_1 = new_df_1.withColumn("base_premium",
                                when((col("VEHICLE_YEAR") == "before 2015"), col("base_premium") * 1.1)
                                .when((col("VEHICLE_YEAR") == "after 2015"), col("base_premium") * 0.95))
    new_df_1.show(5)

    # Calcul de la prime d'assurance 
    

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when((col('AGE') >= 18) & (col('AGE') <= 25), 1.2)
                                .when((col('AGE') >= 26) & (col('AGE') <= 50), 1.0)
                                .when(col('AGE') > 50, 0.8)
                                .otherwise(1.0))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('DRIVING_EXPERIENCE') < 3, col('risk_coefficient') * 1.2)
                                .when(col('DRIVING_EXPERIENCE') >= 10, col('risk_coefficient') * 0.8)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('SPEEDING_VIOLATIONS') > 3, col('risk_coefficient') * 1.2)
                                .when(col('DUIS') > 0, col('risk_coefficient') * 1.5)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('VEHICLE_TYPE') == 'sports car', col('risk_coefficient') * 1.2)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('VEHICLE_OWNERSHIP') == 1, col('risk_coefficient') * 0.9)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('VEHICLE_YEAR') > 2015, col('risk_coefficient') * 1.1)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('risk_coefficient',
                                when(col('PAST_ACCIDENTS') > 0, col('risk_coefficient') * 1.3)
                                .otherwise(col('risk_coefficient')))

    new_df_1 = new_df_1.withColumn('insurance_premium', col('base_premium') * col('risk_coefficient'))

    new_df_1.select('ID', 'AGE', 'risk_coefficient', 'insurance_premium', 'base_premium').show(5)

    # Arrondissons deux chiffres après la virgule le calcul de la base premium 


    new_df_1 = new_df_1.withColumn("base_premium_rounded", round(col("base_premium"), 2))
    new_df_1 = new_df_1.withColumn("insurance_premium_rounded", round(col("insurance_premium"), 2))
    new_df_1 = new_df_1.withColumn("risk_coefficient_rounded", round(col("risk_coefficient"), 2))
    #new_df_1.select('risk_coefficient_rounded', 'insurance_premium_rounded', 'base_premium_rounded').show(5)


    return new_df_1.select('risk_coefficient_rounded', 'insurance_premium_rounded', 'base_premium_rounded')

