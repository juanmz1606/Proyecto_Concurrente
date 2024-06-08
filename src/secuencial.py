import argparse
import time
from Bio import SeqIO
from PIL import Image

def dotplot_secuencial(seq1, seq2):
    dotplot = [[0 for _ in range(len(seq2))] for _ in range(len(seq1))]

    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                dotplot[i][j] = 1

    return dotplot

def guardar_dotplot_txt(dotplot, file_output):
    with open(file_output, 'w') as f:
        for fila in dotplot:
            f.write(' '.join(map(str, fila)) + '\n')

def guardar_dotplot_imagen(dotplot, file_output):
    img = Image.new('1', (len(dotplot[0]), len(dotplot)))
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = dotplot[j][i]

    img.save(file_output)

def main():
    parser = argparse.ArgumentParser(description='Dotplot secuencial')
    parser.add_argument('--file1', required=True, help='Archivo FASTA 1')
    parser.add_argument('--file2', required=True, help='Archivo FASTA 2')
    parser.add_argument('--num_seqs', type=int, default=100, help='Número de secuencias a tomar de cada archivo FASTA')
    parser.add_argument('--output_txt', required=True, help='Archivo de salida de texto')
    parser.add_argument('--output_img', required=True, help='Archivo de salida de imagen')
    args = parser.parse_args()

    # Cargar secuencias desde archivos FASTA
    seq1 = [record.seq[:1000] for record in SeqIO.parse("data/" + args.file1, 'fasta')][0]
    seq2 = [record.seq[:1000] for record in SeqIO.parse("data/" + args.file2, 'fasta')][0]
    
    # Calcular dotplot
    start_time = time.time()
    dotplot = dotplot_secuencial(seq1, seq2)
    end_time = time.time()

    print(f"Tiempo de ejecución: {end_time - start_time} segundos")

    # Guardar dotplot en archivo de texto
    guardar_dotplot_txt(dotplot, args.output_txt)

    # Guardar dotplot como imagen
    guardar_dotplot_imagen(dotplot, args.output_img)

if __name__ == '__main__':
    main()
