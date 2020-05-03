# Uso esta sintaxis porque con "!" no me funciona

# Primer archivo de celulas tumorales
system("python -m HTSeq.scripts.count -s no -f bam ARID2_1.filtered.bam Reduced_genes.gtf > ARID2_1.counts", 
       intern=TRUE)

# Segundo archivo de celulas tumorales
system("python -m HTSeq.scripts.count -s no -f bam ARID2_2.filtered.bam Reduced_genes.gtf > ARID2_2.counts", 
       intern=TRUE)

# Tercer archivo de celulas tumorales
system("python -m HTSeq.scripts.count -s no -f bam ARID2_3.filtered.bam Reduced_genes.gtf > ARID2_3.counts", 
       intern=TRUE)

# Cuarto archivo de celulas tumorales
system("python -m HTSeq.scripts.count -s no -f bam ARID2_4.filtered.bam Reduced_genes.gtf > ARID2_4.counts", 
       intern=TRUE)

# Primer archivo de celulas de tejido sano de control
system("python -m HTSeq.scripts.count -s no -f bam Control_1.filtered.bam Reduced_genes.gtf > Control_1.counts", 
       intern=TRUE)

# Segundo archivo de celulas de tejido sano de control
system("python -m HTSeq.scripts.count -s no -f bam Control_2.filtered.bam Reduced_genes.gtf > Control_2.counts", 
       intern=TRUE)

# Tercer archivo de celulas de tejido sano de control
system("python -m HTSeq.scripts.count -s no -f bam Control_3.filtered.bam Reduced_genes.gtf > Control_3.counts", 
       intern=TRUE)

# Cuarto archivo de celulas de tejido sano de control
system("python -m HTSeq.scripts.count -s no -f bam Control_4.filtered.bam Reduced_genes.gtf > Control_4.counts", 
       intern=TRUE)

# Verifico si está todo
system("ls -lrt", intern=TRUE)

# Preparo una variable con los nombres de los ficheros .counts que hemos preparado en el paso anterior
samples<- c(paste0("ARID2_",1:4),paste0("Control_",1:4))
samples

# Preparo la primera columna de la tabla, con los números de la primera muestra
# y los indices, que representan los genes
first_sample <- read.delim(paste0(samples[1],".counts"),header=F,row.names=1)
head(first_sample)

# Transformo la columna en un data frame
dataframe <- data.frame(first_sample)

# Añado las demás columnas
for (s in samples[2:length(samples)]){ 
    file <- paste0(s,".counts")
    column <- read.delim(file,header=F,row.names=1)
    dataframe <- cbind(dataframe,s=column) 
}

# Cambio los nombre de las columnas del data frame usando la variable 'samples' que he creado antes    
colnames(dataframe) <- samples

head(dataframe)

grp <- c(rep("ARID2",4),rep("Control",4))

cData <- data.frame(sample_Type=as.factor(grp))

rownames(cData) <- colnames(dataframe)

grp
cData

library("DESeq2")

d.deseq <- DESeqDataSetFromMatrix(countData=dataframe,colData=cData,design=~sample_Type)
d.deseq

d.deseq$sample_Type <-relevel(d.deseq$sample_Type, ref="Control")

ARID2_DESeq <- DESeq(d.deseq)
ARID2_DESeq

res <- results(ARID1A_DESeq)
res

plotMA(res)

write.table(res,"ARID2_results.txt",sep="\t", col.names=NA)

Norm_ARID2 <- estimateSizeFactors(ARID2_DESeq)

c <- counts(Norm_ARID2,normalized=TRUE)

write.table(c,"ARID2_expresion_normalizada.txt",sep="\t",col.names=NA)
