# bitcoin_blockchain_parser
This project utilizes a simple parser for the bitcoin's blockchain and a few steps and tricks that can convert the raw Bitcoin blockchain (.dat) in a compact and uniform dataset, that can be easily analyzed in terms of distinct transactions or addresses. 

As a result, each transaction entry is simplified to a quadruple, which includes the following:
1. the transaction id (identifier for the transaction hash)
2. the public key id (identifier of the address)
3. the value transferred (specifying if sent or received)
4. the timestamp

The steps are described in the run_full_scale bash script, and the main idea is the following:
Running the main parser will give as output 3 files, inputs.csv outputs.csv and transactions.csv. In blockchain approaches, a feature is that each input has a reference to a previous output in order to be valid, thus in order to bind an input to an output one need to parse the entire blockchain to find this specific reference. This is solved in the fastest way possible here with only a few full iterations of the csv files.
In sort, the inputs.csv and outputs.csv are merged, while previously the transaction hash(reference) was also added in the outputs.csv file. Then, after sorting the final file using as keys the transaction hash, it is safe to say that 2 continious lines with the same transaction hash are an input and the corresponding output.

