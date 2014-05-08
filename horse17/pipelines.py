from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy import log
import time

class DropIfExpiredPipeline(object):
    def process_item(self, item, spider):
        #TODO expired?
        if all(item.values()):
            raise DropItem()
        else:
            return item

class Horse17Pipeline(object):
    def process_item(self, item, spider):
        print 'pipeline processing'
        return item

class MysqlStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'meixun',
            user = 'root',
            passwd = '',
            charset = 'UTF8',
            use_unicode = True,
            cursorclass = MySQLdb.cursors.DictCursor
        )
    def process_item(self,item,spider):
        d = self.dbpool.runInteraction(self._do_upsert,item,spider)
        d.addErrback(self._handle_err,item,spider)
        d.addBoth(lambda _:item)
        return d
    def _do_upsert(self,conn,item,spider):
        """Perform an insert or update"""
        conn.execute("""select * from event 
                where website = %s""",(item['source_url'],))
        print 'db writer processing'
        ret = conn.fetchone()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        if ret:
            spider.log("Event has exists: [%s] <<< [%s] " 
                    % (item['title'], item['source_url']))
        else:
            conn.execute("""INSERT INTO event (logo,title,performer,organizer,
                    organizerlink,starttime,endtime,desctiption,city,district,
                    address,images,tags,tel,email,website,qq,weichat,`loop`,groups
                    ,hot,lastupdate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (item['logo'],item['title'],item['performer'],item['organizer'],
                    item['organizerlink'],item['starttime'],item['endtime'],
                    item['description'],item['city'],item['district'],
                    item['address'],item['image'],item['tags'],item['tel'],
                    item['email'],item['source_url'],item['qq'],item['weichat'],
                    item['loop'],item['groups'],item['hot'],now))
            
    def _handle_err(self,failture,item,spider):
        """Handle occured on db interaction"""
        # just log
        log.err(failture)
