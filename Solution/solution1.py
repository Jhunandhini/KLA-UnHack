import csv
import math

def read_care_areas(file_path):
    care_areas = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            care_areas.append({
                'id': int(row[0]),
                'x1': float(row[1]),
                'x2': float(row[2]),
                'y1': float(row[3]),
                'y2': float(row[4]),
                'x_center': (float(row[1]) + float(row[2])) / 2,
                'y_center': (float(row[3]) + float(row[4])) / 2
            })
    return care_areas

def read_meta_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        meta_data = next(reader)
        main_field_size = float(meta_data[0])
        sub_field_sizes = [float(size) for size in meta_data[1].split()]
    return main_field_size, sub_field_sizes

def place_main_fields(care_areas, main_field_size):
    main_fields = []

    for area in care_areas:
        x_center = area['x_center']
        y_center = area['y_center']
        main_field = {
            'x1': x_center - main_field_size / 2,
            'x2': x_center + main_field_size / 2,
            'y1': y_center - main_field_size / 2,
            'y2': y_center + main_field_size / 2
        }
        main_fields.append(main_field)

    return main_fields

def place_sub_fields(care_areas, main_fields, sub_field_size):
    sub_fields = []

    for main_field in main_fields:
        for care_area in care_areas:
            if care_area['x1'] >= main_field['x1'] and care_area['x2'] <= main_field['x2'] and care_area['y1'] >= main_field['y1'] and care_area['y2'] <= main_field['y2']:
                x_start = care_area['x1']
                y_start = care_area['y1']
                x_end = care_area['x2']
                y_end = care_area['y2']

                x_positions = [x_start + i * sub_field_size for i in range(math.ceil((x_end - x_start) / sub_field_size))]
                y_positions = [y_start + i * sub_field_size for i in range(math.ceil((y_end - y_start) / sub_field_size))]

                for x in x_positions:
                    for y in y_positions:
                        sub_field = {
                            'x1': x,
                            'x2': x + sub_field_size,
                            'y1': y,
                            'y2': y + sub_field_size,
                            'parent_id': main_field['id']
                        }
                        if sub_field['x2'] <= main_field['x2'] and sub_field['y2'] <= main_field['y2']:
                            sub_fields.append(sub_field)

    return sub_fields

def write_main_fields(main_fields, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Xmin', 'Xmax', 'Ymin', 'Ymax'])
        for mf_id, main_field in enumerate(main_fields):
            writer.writerow({'ID': mf_id, 'Xmin': main_field['x1'], 'Xmax': main_field['x2'], 'Ymin': main_field['y1'], 'Ymax': main_field['y2']})

def write_sub_fields(sub_fields, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'ParentID'])
        for sf_id, sub_field in enumerate(sub_fields):
            writer.writerow({'ID': sf_id, 'Xmin': sub_field['x1'], 'Xmax': sub_field['x2'], 'Ymin': sub_field['y1'], 'Ymax': sub_field['y2'], 'ParentID': sub_field['parent_id']})

def main():
    care_areas = read_care_areas(r'Milestone1\Data\CareAreas.csv')
    main_field_size, sub_field_sizes = read_meta_data(r'Milestone1\\Data\metadata.csv')

    main_fields = place_main_fields(care_areas, main_field_size)
    for idx, field in enumerate(main_fields):
        field['id'] = idx

    sub_field_size = sub_field_sizes[0]  
    sub_fields = place_sub_fields(care_areas, main_fields, sub_field_size)

    write_main_fields(main_fields, r'Milestone1\Solution\mainfields.csv')
    write_sub_fields(sub_fields, r'Milestone1\Solution\subfields.csv')

    print(f"Total subfields placed: {len(sub_fields)}")

if __name__ == '__main__':
    main()
