
def apply_column_mapping(data, config):

    mapping_config = config["column_mapping"]

    transformed_data = {}

    for dataset_name, df in data.items():

        if dataset_name in mapping_config:

            column_mapping = mapping_config[dataset_name]

            df = df.rename(columns=column_mapping)

        transformed_data[dataset_name] = df

        print("Mapping completed:", dataset_name)

    return transformed_data
