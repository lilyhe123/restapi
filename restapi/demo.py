
with open("udd.new", "w") as outs:
    with open("udd.out", "r") as ins:
        array = []
        for line in ins:
            if line.find('BEA-000000') != -1:
                outs.write(line[line.find('BEA-000000')+12:])



