import re


# Files
sample = open(sys.argv[1], 'r')
control = open(sys.argv[2], 'r')
FP_log_name = str(sys.argv[1]) + "_false_positives.txt"
FP_log = open(FP_log_name,'w')
FP_log_name = str(sys.argv[1]) + "_matched_results.txt"
matched_log = open(FP_log_name,'w')

temoin = open('mutations.vcf', 'r')
sample = open('variants_amp80.vcf', 'r')

identified = 0
false_negative = 0
control_list = []



# Create list from lines in sample
sample_list = []
for line in sample.readlines():
	print(line)
	try:
		sample_pos = re.findall(sample_regex, line)[0]
		sample_chr = re.findall(chromosome_regex, line)[0]
		sample_key = str(sample_chr) + str(sample_pos)
		sample_list.append(sample_key)
	except:
		pass



control_dict = {}
mutation = ""
clone = ""

somatic_list = open(str(sample_name + "_somatic_list.txt"), "w")
germline_list = open(str(sample_name + "_germline_list.txt"), "w")
somatic_control_count = 0
germline_control_count = 0
control_total_count = 0

for line in control:
	try:
		control_pos = re.findall(control_regex, line)[0]
		control_chr = re.findall(chromosome_regex, line)[0]
		control_dict_key = str(control_chr) + str(control_pos)
		control_total_count += 1


		chrType = re.findall(origin_regex, line)[0]
		if chrType == "A" or "B":
			somatic_list.write(line)
			somatic_control_count += 1
		elif chrType == "germline|A|B":
			clone = "Clone Germline"
			germline_list.write(line)
			germline_control_count += 1

	except:
			pass

# Print results
print("\n################# S T A T S ##################\n")
print(" True Pos : " + str(true_positive) + " = " + str(true_positive_verify))
print(" False Neg : " + str(false_negative))
print(" Total mutations in Control : " + str(false_negative + true_positive) + " = " + str(control_id_count))
print(" Total mutations in Sample : " + str(sample_list_count))
print(" False Positives : " + str(false_positive))
print(" Sensitivity : " + str(100 * true_positive / (true_positive + false_negative)) + " %")
print(" Precision : " + str(100 * true_positive / (true_positive + false_positive)) + " %")
print("\n##############################################\n")
FP_log.close()
matched_log.close()



		control_dict_value = str(clone) + "|| \t ||" + str(mutation) + "||"
		control_dict.update({control_dict_key:control_dict_value})
	except:
		pass


# DETECT FALSE POSITIVES
false_positive = 0
for line in sample:
	try:
		sample_chr = re.findall(chromosome_regex, line)[0]
		sample_pos = re.findall(sample_regex, line)[0]
		sample_key = str(sample_chr) + str(sample_pos)

		if sample_key not in control_dict.keys():
			false_positive += 1

	except:
		pass


# DETECT FALSE NEGATIVES
true_positive = 0
for key in control_dict.keys():
	if key in sample_list:
		true_positive += 1
	else:
		false_negative += 1



for line in iter(temoin):
	temoin_pos = re.findall(temoin_regex, line)
	if temoin_pos:
		for line in iter(sample):
			sample_pos = re.findall(sample_regex, line)
			if sample_pos:
				if sample_pos[0] == temoin_pos[0]:
					identified = identified + 1
					print(str(identified))
				else:
					print("temoin: " + str(temoin_pos[0]) + " | sample: " + str(sample_pos[0]))


	# print("looking for position : " + str(temoin_pos))




# for line in temoin:
# 	temoin_pos = re.findall(temoin_regex, line)[0]
# 	print("looking for position : " + str(temoin_pos))
# 	for line in sample:
# 		myPos_d = re.findall(sample_regex, line)
# 		try:
# 			myPos_d = myPos_d[0]

# 		except Exception:
# 			pass

# 		if temoin_pos == myPos_d:
# 			print(temoin_pos + " found in " + myPos_d)
# 			identified = identified + 1