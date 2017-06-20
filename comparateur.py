import re

# Define the program
def stat_program(filename):
	sample = open(filename, 'r')
	noext_filename = os.path.splitext(os.path.basename(filename))[0]
	# Files
	# sample = open(sys.argv[1], 'r')
	control = open(sys.argv[2], 'r')
	FP_log_name = str(noext_filename) + "_false_positives.txt"
	FP_log = open(FP_log_name,'w')
	FP_log_regex = open(str(noext_filename) + "_false_positives" + "_regex.txt",'w')
	matched_log_name = str(noext_filename) + "_matched_results.txt"
	matched_log = open(matched_log_name,'w')

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
	for line in sample:
		if not line.startswith("#", 0, 1):
			split_line = line.split("\t")
			sample_chr = split_line[0]
			sample_pos = split_line[1]
			sample_alt = split_line[3]
			sample_id = str(sample_chr) + "_" + str(sample_pos) + "_" + str(sample_alt)
			sample_id = sample_id.replace(" ", "")
			FP_log_regex.write("(" + str(sample_pos) + ")|")
			if sample_id not in sample_id_list:
				sample_id_list.append(sample_id)



	# Find true positives and false negatives by comparing Control > sample
	for line in control:
		if not line.startswith("#", 0, 1):
			control_id_count +=1
			split_line = line.split("\t")
			control_chr = split_line[0]
			control_pos = split_line[1]
			control_alt = split_line[3]
			control_origin = split_line[7]
			control_id = str(control_chr) + "_" + str(control_pos) + "_" + str(control_alt)
			control_id = control_id.replace(" ", "")
			if control_id not in control_id_list:
				control_id_list.append(control_id)
				origin_dict.update({control_id:control_origin})
			if control_id in sample_id_list:
				true_positive += 1
			else:
				false_negative += 1



	# Find false positives
	for item in sample_id_list:
		sample_list_count += 1
		if item not in control_id_list:
			false_positive += 1
			FP_log.write(str(item) + "\n")
		else:
			matched_log.write(str(item) + "\t" + str(origin_dict[item]))
			true_positive_verify +=1



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
	print(" Sensitivity : " + str(100 * true_positive / (true_positive + false_negative)) + " %")
	results_log.write("\n Sensitivity : " + str(100 * true_positive / (true_positive + false_negative)) + " %")
	print(" Precision : " + str(100 * true_positive / (true_positive + false_positive)) + " %\n")
	results_log.write("\n Precision : " + str(100 * true_positive / (true_positive + false_positive)) + " %\n")

	FP_log.close()
	FP_log_regex.close()
	matched_log.close()

	# testsubject = str(sys.argv[2])
	# FP_log_regex = open((str(noext_filename) + "_false_positives" + "_regex.txt"),'r').read()
	# FP_log_regex = "sed \"/" + FP_log_regex + "/p\" " + str(testsubject) + " > " + str(testsubject) + "_matches.txt"
	# print(FP_log_regex)
# End of function






results_log = open("table_results.txt",'w')

print("\n################# S T A T S ##################")
results_log.write("\n################# S T A T S ##################")

# Execute the program with the inputted files
if os.path.isdir(sys.argv[1]) == False:
	stat_program(sys.argv[1])

else:
	for filename in os.listdir(sys.argv[1]):
		filename_path = str(sys.argv[1]) + "/" + str(filename)
		stat_program(filename_path)

print("\n##############################################\n")
results_log.write("\n##############################################\n")
