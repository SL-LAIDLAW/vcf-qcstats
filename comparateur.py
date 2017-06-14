import re



temoin_regex = r"(?:\d|\w)(?:\s)(\d*)"
sample_regex = r"(?:\w\s)(\d*)"

temoin = open('mutations.vcf', 'r')
sample = open('variants_amp80.vcf', 'r')

identified = 0


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