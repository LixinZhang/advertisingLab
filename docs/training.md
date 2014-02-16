#Training Data Format
###Each line consists of fields delimited by the TAB character
1. Click : the number of times, among the above impressions, the user (UserID) clicked the ad (AdID)
* Impression : the number of search sessions in which the ad (AdID) was impressed by the user (UserID) who issued the query (Query).
* Display URL :a property of the ad
    
    The URL is shown together with the title and description of an ad. It is usually the shortened landing page URL of the ad, but not always. In the data file,  this URL is hashed for anonymity. 
* AdID :
* AdvertiserID : a property of the ad
* Depth : The number of ads impressed in a session is known as the 'depth'
* Position : The order of an ad in the impression list is known as the ‘position’ of that ad.
*  QueryID : id of the query

	This id is a zero‐based integer value. It is the key of the data file 'queryid_tokensid.txt'.
* KeywordID : a property of ads 

	This is the key of  'purchasedkeyword_tokensid.txt'. 
* TitleID : a property of ads
	
	This is the key of 'titleid_tokensid.txt'. 
* DescriptionID : a property of ads. 

	This is the key of 'descriptionid_tokensid.txt'.
* UserID : 
 
 	This is the key of 'userid_profile.txt'.  When we cannot identify the user, this field has a special value of 0. 
   
