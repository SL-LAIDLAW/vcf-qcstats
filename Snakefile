DIR = "."
control = 'controlGP.vcf'
sample = 'variants_amp70.vcf'

rule final:
    input:
       plots = "Rplots.pdf"


rule quantify_genes:
    input:
        c = control,
        s = sample

    output:
        sort = "variants_amp70_sorted.vcf",
        table = "variants_amp70_quality_table.txt"


    shell:
        "python comparateur.py {input.s} {input.c} snakefile"


rule generate_plots:
    input:
        t = "variants_amp70_quality_table.txt",
        r = "plot.R"

    output:
        "Rplots.pdf"

    shell:
        "Rscript --vanilla {input.r} {input.t}"
