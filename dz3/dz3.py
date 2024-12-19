import argparse
import toml

def parse_toml(file_path):
    try:
        with open(file_path, 'r') as file:
            return toml.load(file)
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {e}")

def convert_to_custom_format(toml_data):
    output_lines = []

    def process_value(value):
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            return "' " + ' '.join(process_value(v) for v in value) + " '"
        elif isinstance(value, dict):
            return ', '.join(f"{k} : {process_value(v)}" for k, v in value.items())
        return ''

    for key, value in toml_data.items():
        if isinstance(value, dict):
            output_lines.append(f"{key} : {{{convert_to_custom_format(value)}}}")
        else:
            output_lines.append(f"{key} : {process_value(value)};")

    return '\n'.join(output_lines)

def main():
    parser = argparse.ArgumentParser(description='Convert TOML to custom configuration language.')
    parser.add_argument('input_file', help='Path to the input TOML file.')
    parser.add_argument('output_file', help='Path to the output configuration file.')

    args = parser.parse_args()

    toml_data = parse_toml(args.input_file)
    custom_format = convert_to_custom_format(toml_data)

    with open(args.output_file, 'w') as file:
        file.write(custom_format)

    print("Успешно")

if __name__ == '__main__':
    main()