const express = require('express');
const router = express.Router();
const upload = require('express-fileupload')
const spawn  = require('child_process').spawn;

const index = express()

const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');

// Welcome Page
router.get('/', forwardAuthenticated, (req, res) => res.render('welcome'));





//=================================================================================
//Connecting to mongodb
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const { callbackify } = require('util');

//Connection URL
const url =  'mongodb://localhost:27017';

//Dababase Name
const dbName = 'mydb';

//Create a new MongoClient
const client = new MongoClient(url);


index.use('/static', express.static('public'));

// EJS
//app.use(expressLayouts);
index.set('view engine', 'ejs');
//=================================================================================




//=====================================DASHBOARD=============================================
router.get('/dashboard', ensureAuthenticated, (req, res) => {
  //let device_list =  [{'name': 'dht22'}, {'name': 'tmp36'}]

  //eval(require('locus'));
  const db = client.db(dbName);
  const collection = db.collection('Publications');

  //Find some documents
  collection.find({}).toArray(function(err, device_list){
      assert.equal(err,null);
      
      // res.render('devices', {'Publications':device_list})
      res.render('dashboard', {'Publications':device_list})
  });


});


//======================================AUTHOR BROWSING PAGE==========================================================


router.get('/authorBrowse',ensureAuthenticated, (req, res) => {
        //let device_list =  [{'name': 'dht22'}, {'name': 'tmp36'}]

        
    
        const db = client.db(dbName);
        const collection = db.collection('PublicationsTable');

        //Find some documents
        collection.distinct("Author", {}, function(err, author_list){
            assert.equal(err,null); 
            
           // res.render('devices', {'Publications':device_list})
           res.render('authorBrowse', {'PublicationsTable':author_list})
         //  console.log(author_list)    
           
    
    }); 
 });


 //======================================AUTHOR BROWSING PAGE 2==========================================================

 router.get('/authorBrowse/:id', (req, res) => {

  const db = client.db(dbName);
  const collection = db.collection('PublicationsTable');
  
  let query =  req.params.id;

  
 
  collection.find({"Author":query}).toArray(function(err, reso){
      assert.equal(err,null); 
       
      res.render('authorData', {'PublicationsTable':reso})
     
}); 
});


 //======================================PROCEEDING BROWSING PAGE==========================================================

 router.get('/proceedingBrowse',ensureAuthenticated, (req, res) => {

    const db = client.db(dbName);
    const collection = db.collection('PublicationsTable');

    //Find some documents
    collection.find({"TypeOfPublication":"Conference"}).toArray(function(err, reso){
        assert.equal(err,null); 
        
        
        res.render('proceedingBrowse', {'PublicationsTable':reso})

}); 
});

//======================================PROCEEDING BROWSING PAGE 2==========================================================

router.get('/proceedingBrowse/:d', (req, res) => {


  const db = client.db(dbName);
  const collection = db.collection('PublicationsTable');
  let query =  req.params.d;

  //Find some documents
  collection.find({"Title":query}).toArray(function(err, reso){
      assert.equal(err,null); 
      
      //res.send('proceedingBrowse');
      res.render('ProceedData', {'PublicationsTable':reso})
      
      console.log(reso);
      console.log(query);

}); 
});








//======================================JOURNAL BROWSING PAGE==========================================================

router.get('/journalBrowse', (req, res) => {
    //let device_list =  [{'name': 'dht22'}, {'name': 'tmp36'}]

    

    const db = client.db(dbName);
    const collection = db.collection('PublicationsTable');

    //Find some documents
    collection.find({"TypeOfPublication":"Journal"}).toArray(function(err, reso){
        assert.equal(err,null); 
        
        
        res.render('journalBrowse', {'PublicationsTable':reso})
     //  console.log(author_list)    
       

}); 
});

//======================================PROCEEDING BROWSING PAGE 2==========================================================

router.get('/journalBrowse/:d1', (req, res) => {


  const db = client.db(dbName);
  const collection = db.collection('PublicationsTable');
  let query =  req.params.d1;
  console.log(query);

  //Find some documents
  collection.find({"Title":query}).toArray(function(err, reso){
      assert.equal(err,null); 
      
      //res.send('proceedingBrowse');
      res.render('JournalData', {'PublicationsTable':reso})
      
      //console.log(reso);
      //console.log(query);

}); 
});



//====================================== BOOK BROWSING PAGE==========================================================

router.get('/bookBrowse', (req, res) => {
    //let device_list =  [{'name': 'dht22'}, {'name': 'tmp36'}]

    

    //const db = client.db(dbName);
    //const collection = db.collection('PublicationsTable');

    //Find some documents
    //collection.find({"TypeOfPublication":"Journal"}).toArray(function(err, reso){
      //  assert.equal(err,null); 
        
        
        res.render('bookBrowse')
     //  console.log(author_list)    
       

//}); 
});


//======================================DHET FILE UPLOAD PAGE==========================================================

router.get('/fileUpload', (req, res) => {

      res.render('fileUpload')
   
});

router.use(upload());
router.get('/fileUpload', (req, res) =>{

  res.sendFile(__dirname + '/fileUpload');

});

router.post('/', (req, res) => {
  if(req.files){
      console.log(req.files);
      var file = req.files.file;
      var filename = file.name;
      console.log(filename);

      /*
      
      const pyScript = spawn('python', ['./upload/script.py']);

      pyScript.stdout.on('data', function(data)
      {
      
        console.log(data.toString());
        res.write(data);
        res.end('end');
      });
        
       */




      file.mv('./upload/'+filename, function(err){
          if(err){
              req.send(err)
          }
          else{
              res.render('fileUpload')
          }
      });
  }
});





module.exports = router;

client.connect(function(err) {
  assert.equal(null, err);
  console.log('Connected succesfully to the Mongo databse');


});