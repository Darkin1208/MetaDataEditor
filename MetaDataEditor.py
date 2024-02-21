import os
import piexif
from PIL import Image
import datetime

def edit_file_metadata(file_path, modification_time, access_time):
    times = (access_time.timestamp(), modification_time.timestamp())
    os.utime(file_path, times)

def edit_image(file_path, selected_options):
    img = Image.open(file_path)

    exif_dict = img.info.get('exif', {})
    
    for option, value in selected_options.items():
        if option in ['artist', 'make', 'model', 'software']:
            value_bytes = value.encode('utf-8') if isinstance(value, str) else value
            exif_dict.setdefault('0th', {}).setdefault(piexif.ImageIFD.__dict__[option.capitalize()], value_bytes)
        elif option == 'exposure_time':
            exif_dict.setdefault(piexif.ExifIFD.ExposureTime, (value, 1000))
        elif option == 'flash':
            exif_dict.setdefault(piexif.ExifIFD.Flash, value)

    edited_file_path = os.path.join('edited_images', f'edited_{os.path.basename(file_path)}')
    img.save(edited_file_path, exif=piexif.dump(exif_dict))

    modification_time = selected_options.get('modification_time')
    access_time = selected_options.get('access_time')

    if modification_time or access_time:
        edit_file_metadata(edited_file_path, modification_time, access_time)

    print(f'A imagem {file_path} foi editada e salva como {edited_file_path}')

def main():
    while True:
        folder_path = 'images'

        edit_options = {
            'artist': "Editar informações do artista",
            'make': "Editar fabricante",
            'model': "Editar modelo",
            'software': "Editar software",
            'exposure_time': "Editar tempo de exposição do flash [1-1000]",
            'flash': "Editar modelo do flash",
            'modification_time': "Editar data de modificação",
            'access_time': "Editar data de acesso",
        }

        selected_options = {}
        for option, description in edit_options.items():
            user_input = input(f"{description} (no formato 'YYYY-MM-DD HH:MM:SS', deixe em branco para não editar): ") if option in ['modification_time', 'access_time'] else input(f"{description} (deixe em branco para não editar): ")
            if user_input:
                selected_options[option] = datetime.datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S') if option in ['modification_time', 'access_time'] else user_input

        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print("\nImagens disponíveis:")
        for i, image_file in enumerate(image_files, 1):
            print(f"{i}. {image_file}")

        selected_indices = [int(index.strip()) for index in input("Digite o número(s) das imagens para editar (separados por vírgula): ").split(',') if index.strip().isdigit()]

        for index in selected_indices:
            if 1 <= index <= len(image_files):
                selected_image_path = os.path.join(folder_path, image_files[index - 1])
                try:
                    edit_image(selected_image_path, selected_options)
                except Exception as e:
                    print(f"Erro ao editar a imagem {selected_image_path}: {e}")

            else:
                print(f"Índice inválido: {index}. Ignorando.")

        more_edits = input("Edição concluída. Pressione Enter para continuar editando ou digite 'exit' para sair: ")
        if more_edits.lower() == 'exit':
            print("Encerrando o programa. Até mais!")
            break

if __name__ == "__main__":
    main()
