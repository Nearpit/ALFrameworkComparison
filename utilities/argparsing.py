from argparse import ArgumentParser, BooleanOptionalAction
    
def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dataset",
                        help="What dataset to train on", 
                        required=True)
    parser.add_argument("-a", "--algorithm",
                        help="What active learning algorithm to evaluate",  
                        choices=["random",
                                 "keychain_naive",
                                 "keychain_autoencoder",
                                 "bald", 
                                 "coreset",
                                 "entropy",
                                 "margin"])
    parser.add_argument("-r", "--random_seed",
                        help="What random seed to use",  
                        type=int,
                        default=42)
    
    parser.add_argument("-vs", "--val_share",
                    help="What share of unviolated labeled instances to use for validation",
                    type=float,
                    default=0.25)
    
    parser.add_argument("-n_il", "--n_initially_labeled",
                    help="What number of labeled instances to start with",
                    type=int,
                    default=20)
    
    parser.add_argument("-o", "--online",
                    help="Are the hyperparameters searched online or they stay static? Options: --online or --no-online",
                    default=True, 
                    action=BooleanOptionalAction)
    
    return parser.parse_args()