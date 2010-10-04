import couchdb
#print couchdb.__version__

couch = couchdb.Server()

if 'travel' in couch:
    db = couch['travel']
else:
    db = couch.create('travel')


place1 = {'type':'place','country':'Greece','city':'Athens'}
place2 = {'type':'place','country':'Greece','city':'Piraeus'}

p1Reval = db.save(place1)
p1Id = p1Reval[0]
p2Reval = db.save(place2)
p2Id = p2Reval[0]

trip1 = {'type':'trip','title':'Athens Marathon 2010', 'startDate':'2010-10-27T17:30:12Z-04:00','endDate':'2010-10-27T17:30:12Z-04:00', 'places' : [p1Id, p2Id]}
db.save(trip1)

mapf = '''
function(doc) {
    if(doc.type == 'trip'){
        emit([doc.title, 0], doc);
        if(doc.places){
            for(var i in doc.places){
                emit([doc.title,1], {_id:doc.places[i]});
            }
        }
    }
}
'''

results = db.query(mapf,None,'javascript',None,include_docs=True)
print results.rows
print "===================="
for r in results.rows:
    print r.value
    print r.doc


couch.delete('travel')
