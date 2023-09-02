/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
    } catch (error) {
        return { error: error.description };
    }
}

main({
    IAM_API_KEY: process.env.CLOUDANT_API_KEY,
    COUCH_URL: process.env.COUCH_URL
}).then(result => {
    console.log(result);
}).catch(error => {
    console.error("Error:", error);
});

/**
 * {
  IAM_API_KEY: "u9YjnNaxZbHBGgxNByVrgLw1T1cPVw6IInZBtqN0TxOm",
  COUCH_URL: "https://4737f811-c189-4729-926f-45de680b14e3-bluemix.cloudantnosqldb.appdomain.cloud"
} 
*/

