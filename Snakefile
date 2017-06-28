DIR = "."
control = 'controlGP.vcf'
sample = 'variants_amp50.vcf'

rule final:
    input:
       plots = "Rplots.pdf"


rule quantify_genes:
    input:
        c = control,
        s = sample

    output:
        sort = "variants_amp50_sorted.vcf",
        table = "variants_amp50_quality_table.txt"


    shell:
        "python comparateur.py -s {input.s} -c {input.c} --snakefile"


rule generate_plots:
    input:
        t = "variants_amp50_quality_table.txt",
        r = "plot.R"

    output:
        "Rplots.pdf"

    shell:
        "Rscript --vanilla {input.r} {input.t}"
