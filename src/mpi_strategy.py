import argparse
import time
from Bio import SeqIO
from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from mpi4py import MPI

def dotplot_secuencial(seq1, seq2, start, end):
    dotplot = [[0 for _ in range(len(seq2))] for _ in range(len(seq1))]

    for i in range(start, end):
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

def aplicar_convolucion(dotplot, filtro):
    return convolve2d(dotplot, filtro, mode='same', boundary='fill', fillvalue=0).tolist()

def main():

    parser = argparse.ArgumentParser(description='Dotplot paralelo')
    parser.add_argument('--file1', required=True, help='Archivo FASTA 1')
    parser.add_argument('--file2', required=True, help='Archivo FASTA 2')
    parser.add_argument('--num_seqs', type=int, default=100, help='Número de secuencias a tomar de cada archivo FASTA')
    parser.add_argument('--output', required=True, help='Archivo de salida')
    parser.add_argument('--outputNoFilter', required=True, help='Archivo de salida sin filtro')

    args = parser.parse_args()

    args.output_txt = args.output + ".txt"
    args.output_img = args.output + ".png"
    args.output_txt_no_f = args.outputNoFilter + ".txt"
    args.output_img_no_f = args.outputNoFilter + ".png"

    # Inicializar MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Cargar secuencias desde archivos FASTA
    seq1 = [record.seq[:1000] for record in SeqIO.parse("data/" + args.file1, 'fasta')][0]
    seq2 = [record.seq[:1000] for record in SeqIO.parse("data/" + args.file2, 'fasta')][0]


    # Dividir el trabajo en sub-secuencias
    num_subseqs = len(seq1) // size
    start = rank * num_subseqs
    end = (rank + 1) * num_subseqs if rank < size - 1 else len(seq1)

    # Calcular dotplot
    start_time = time.time()
    dotplot = dotplot_secuencial(seq1, seq2, start, end)
    end_time = time.time()

    print(f"Tiempo de ejecución en proceso {rank}: {end_time - start_time} segundos")

    # Aplicar convolución
    filtro_diagonal = np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]])

    dotplot_diagonal = aplicar_convolucion(dotplot, filtro_diagonal)

    # Guardar dotplot en archivo de texto
    guardar_dotplot_txt(dotplot, args.output_txt_no_f)

    # Guardar dotplot como imagen
    guardar_dotplot_imagen(dotplot, args.output_img_no_f)

    # Guardar dotplot en archivo de texto
    guardar_dotplot_txt(dotplot_diagonal, args.output_txt)

    # Guardar dotplot como imagen
    guardar_dotplot_imagen(dotplot_diagonal, args.output_img)

if __name__ == '__main__':
    main()
