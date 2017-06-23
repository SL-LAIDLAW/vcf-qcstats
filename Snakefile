# rule quantify_genes:
#     input:
#         control = 'controlGP.vcf',
#         sample = 'variants_amp80.vcf',

#     shell:
#         "python comparateur.py {input.sample} {input.control}"

DIR = "."
control = 'controlGP.vcf'
sample = 'variants_amp80.vcf'
# table = "variants_amp80_quality_table.txt"

rule final:
    input:
       plots = "Rplots.pdf"


rule quantify_genes:
    input:
        c = control,
        s = sample
    
    output:
        sort = "variants_amp80_sorted.vcf",
        table = "variants_amp80_quality_table.txt"


    shell:
        "python comparateur.py {input.s} {input.c}"


rule generate_plots:
    input:
        t = "variants_amp80_quality_table.txt",
        r = "plot.R"

    output:
        "Rplots.pdf"

    shell:
        "Rscript --vanilla {input.r} {input.t}"
        
#Generation des plot(Rcode)

# data=read.table("/Users/leuks/Lucas/SeqOne/Projets/data/fauxneg", ";")
# ggplot(data, aes(x=Quality, color=Category)) + geom_freqpoly()
# ggplot(data, aes(x=Quality, fill=Category)) + geom_density(alpha=.3)
# dev.print(png, 'variant_COUNT.png',width = 600)
# dev.print(png, 'variant-DENSITY.png',width = 600)