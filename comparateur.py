 #!/usr/bin/python
 # -*- coding: utf-8 -*-
 # Version 1.20

import argparse
import sys
import re

# Define the program
def stat_program(filename):
	sample = open(filename, 'r')
	noext_filename = os.path.splitext(os.path.basename(filename))[0]
	control = open(args['control'], 'r')
	quality_table_name = str(noext_filename) + "_quality_table.txt"
	quality_table = open(quality_table_name,'w')

	if snakefile == False:
			quality_table = open("variants_amp80_quality_table.txt",'w')
			FP_log_name = str(noext_filename) + "_false_positives.txt"
			FP_log = open(FP_log_name,'w')
			FN_log_name = str(noext_filename) + "_false_negatives.txt"
			FN_log = open(FN_log_name,'w')
			FP_log_regex = open(str(noext_filename) + "_false_positives" + "_regex.txt",'w')
			matched_log_name = str(noext_filename) + "_matched_results.txt"
			matched_log = open(matched_log_name,'w')
			quality_TP_log_name = str(noext_filename) + "_TP_quality.txt"
			quality_TP_log = open(quality_TP_log_name,'w')
			quality_FP_log_name = str(noext_filename) + "_FP_quality.txt"
			quality_FP_log = open(quality_FP_log_name,'w')



	# variables
	origin_dict = {}
	sample_id_list = []
	control_id_list = []
	false_negative = 0
	true_positive = 0
	control_id_count = 0
	false_positive = 0
	sample_list_count = 0
	true_positive_verify = 0

	cmd = str("sort -u " + str(filename) + " > " + str(noext_filename) + "_sorted.vcf")
	os.system(cmd)

	sample.close()
	sample = open(str(noext_filename) + "_sorted.vcf", 'r')

	# Create sample list to later be deduplicated
	sampleExt = str(args['sample'])
	sampleExt = sampleExt[-3:]
	print(sampleExt)
	# if vcf then use standardised vcf columns
	if sampleExt == "vcf":
		for line in sample:
			if not line.startswith("#", 0, 1):
				split_line = line.split("\t")
				sample_chr = split_line[0]
				sample_pos = split_line[1]
				# print(str(sample_pos))
				sample_alt = split_line[3]
				sample_qual = split_line[5]
				sample_id = str(sample_chr) + "_" + str(sample_pos) + "_" + str(sample_alt)
				sample_id = sample_id.replace(" ", "")
				sample_id = sample_id.upper()
				if snakefile == False:
					FP_log_regex.write("(" + str(sample_pos) + ")|")
				if sample_id not in sample_id_list:
					sample_id_list.append(sample_id)
					quality_dict_entry = {sample_id : sample_qual}
					quality_dict.update(quality_dict_entry)


	print("\n\n\n")

	# Find true positives and false negatives by comparing Control > sample
	for line in control:
		if not line.startswith("#", 0, 1):
			control_id_count +=1
			split_line = line.split("\t")
			control_chr = split_line[0]
			control_pos = split_line[1]
			print(str(control_pos))
			control_alt = split_line[3]
			control_origin = split_line[7]
			control_id = str(control_chr) + "_" + str(control_pos) + "_" + str(control_alt)
			control_id = control_id.replace(" ", "")
			control_id = control_id.upper()
			if control_id not in control_id_list:
				control_id_list.append(control_id)
				origin_dict.update({control_id:control_origin})
			if control_id in sample_id_list:
				true_positive += 1
			else:
				false_negative += 1
				if snakefile == False:
					FN_log.write(line)



	# Find false positives
	for item in sample_id_list:
		sample_list_count += 1
		if item not in control_id_list:
			false_positive += 1
			if snakefile == False:
				FP_log.write(str(item) + "\n")
				quality_FP_log.write(str(quality_dict[item]) + "\n")
			quality_table.write(str(quality_dict[item]) + "\t" + "FP" + "\n")
		else:
			if snakefile == False:
				matched_log.write(str(item) + "\t" + str(origin_dict[item]))
				quality_TP_log.write(str(quality_dict[item]) + "\n")
			quality_table.write(str(quality_dict[item]) + "\t" + "TP" + "\n")
			true_positive_verify +=1


	if snakefile == False:
		# Print results
		print("\n ### Results for sample : " + str(filename))
		results_log.write("\n ### Results for sample : " + str(filename))
		print(" True Pos : " + str(true_positive) + " = " + str(true_positive_verify))
		results_log.write("\n True Pos : " + str(true_positive) + " = " + str(true_positive_verify))
		print(" False Neg : " + str(false_negative))
		results_log.write("\n False Neg : " + str(false_negative))
		print(" Total mutations in Control : " + str(false_negative + true_positive) + " = " + str(control_id_count))
		results_log.write("\n Total mutations in Control : " + str(false_negative + true_positive) + " = " + str(control_id_count))
		print(" Total mutations in Sample : " + str(sample_list_count))
		results_log.write("\n False Positives : " + str(false_positive))
		print(" False Positives : " + str(false_positive))
		results_log.write("\n False Positives : " + str(false_positive))
		result_sensitivity = 100 * true_positive / (true_positive + false_negative)
		print(" Sensitivity : " + str(result_sensitivity) + " %")
		results_log.write("\n Sensitivity : " + str(result_sensitivity) + " %")
		result_precision = 100 * true_positive / (true_positive + false_positive)
		print(" Precision : " + str(result_precision) + " %")
		results_log.write("\n Precision : " + str(result_precision) + " %")
		print(" F-Score : " + str(2*((result_precision * result_sensitivity)/(result_precision + result_sensitivity)) ))
		results_log.write("\n F-Score : " + str(2*((result_precision * result_sensitivity)/(result_precision + result_sensitivity)) ) + "\n")


		FP_log.close()
		FP_log_regex.close()
		matched_log.close()
		quality_TP_log.close()

		testsubject = str(args['control'])
		FP_log_regex = open((str(noext_filename) + "_false_positives" + "_regex.txt"),'r').read()
		FP_log_regex = "sed \"/" + FP_log_regex + "/p\" " + str(testsubject) + " > " + str(testsubject) + "_matches.txt"
		# print(FP_log_regex)
# End of function


# Parse arguments
parser = argparse.ArgumentParser(description="Sean's magic tool to compare sample and control vcf to determine simple statistics.")
parser.add_argument('-s','--sample', help='--sample [sample.vcf]', required=True)
parser.add_argument('-c','--control', help='the control file to test the sample against \n --control [control.vcf]', required=True)
parser.add_argument('--snakefile',  action='store_true', help='When activated, script will only generate the files necessary for the snakefile', required=False)
args = vars(parser.parse_args())

if bool(args['snakefile']) == True:
	snakefile = True
else:
    snakefile = False


if snakefile == False:
	results_log = open("table_results.txt",'w')
	print("\n################# S T A T S ##################")
	results_log.write("\n################# S T A T S ##################")

# Execute the program with the inputted files
if os.path.isdir(args['sample']) == False:
	stat_program(args['sample'])

else:
	for filename in os.listdir(args['sample']):
		filename_path = str(args['sample']) + "/" + str(filename)
		stat_program(filename_path)

if snakefile == False:
	print("\n##############################################\n")
	results_log.write("\n##############################################\n")
