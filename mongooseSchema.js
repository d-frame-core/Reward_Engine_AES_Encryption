const totalUsersRewardedSchema = mongoose.Schema({
    useraddress:{
        type:Number
    },
    datashared: {
        type: Number,
    },
    DFT:{
        type:Number
    },
    restOFTheData:{
        
    }
});

//Mongoose Schema for the MongoDb where the Data will come from Kafka look like this for every user.

//datashared field is used to set previously data shared by the the user, so that we can compare current data shared and prvoiusle data shared and
//give rewards to those user who actually shared the data.

//DFT field is used to set the total DFTs user got for the data they shared and will be transfered(DFT) once in a month using transferToken() function.

//userAddress field will have the wallet address of the user throught which they logged in