const path = require('path');
const Koa = require('koa2');
const app = new Koa();
const render = require('koa-ejs');
const bodyParser = require('koa-bodyparser');
const Router = require('koa-router');
const serve = require('koa-static');
var router = new Router();
const mysql = require('mysql');
const db = require('./dbconfig')
const pify = require('promise.ify');
const querystring = require('querystring');
var connection = mysql.createConnection(db);
connection.connect();

app.use(bodyParser());
app.use(serve(__dirname+"/static"));
render(app, {
    root: path.join(__dirname, 'view'),
    layout: '__layout',
    viewExt: 'html',
    cache: false,
    debug: false
});
router.get('/', async (ctx)=>{
	sql = 'SELECT conference,COUNT(*) as count FROM article GROUP BY conference;';
	const results = await pify(connection.query,connection)(sql);
	//console.log(results[0][0]['count']);
    await ctx.render('index', {data:results[0], layout:false});
});
router.get('/home', async (ctx)=>{
	sql = 'SELECT conference,COUNT(*) as count FROM article GROUP BY conference;';
	const results = await pify(connection.query,connection)(sql);
	//console.log(results[0][0]['count']);
    await ctx.render('index', {data:results[0], layout:false});
});
router.get('/arXiv', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2018;
		parsed['month'] = 4;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='arXiv' and a.year="+ parsed['year'].toString() + " and a.month="+parsed['month'].toString()+" "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('arXiv', {data:results[0], year:parsed['year'], month:parsed['month'], layout:false});
});
router.get('/CVPR', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2017;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='CVPR' and a.year="+ parsed['year'].toString() + " "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('CVPR', {data:results[0], year:parsed['year'], layout:false});
});
router.get('/ICCV', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2017;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='ICCV' and a.year="+ parsed['year'].toString() + " "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('ICCV', {data:results[0], year:parsed['year'], layout:false});
});
router.get('/ICML', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2017;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='ICML' and a.year="+ parsed['year'].toString() + " "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('ICML', {data:results[0], year:parsed['year'], layout:false});
});
router.get('/NIPS', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2017;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='NIPS' and a.year="+ parsed['year'].toString() + " "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('NIPS', {data:results[0], year:parsed['year'], layout:false});
});
router.get('/ICLR', async (ctx)=>{
	url = ctx.request.url;
	url = url.substr(url.indexOf('?')+1);
	parsed = querystring.parse(url);
	if(parsed['year'] === undefined){
		parsed['year'] = 2017;
	}
	sql = "SELECT a.*,GROUP_CONCAT(au.name) as authors "+
	"from article as a JOIN author as au JOIN relationship as r "+
	"WHERE au.id=r.authorid and a.id=r.articleid and conference='ICLR' and a.year="+ parsed['year'].toString() + " "+
	"and a.abstract like '%person%re-id%' GROUP BY a.id;"
	const results = await pify(connection.query,connection)(sql);
	console.log(results[0][0]);
    await ctx.render('ICLR', {data:results[0], year:parsed['year'], layout:false});
});

app.use(router.routes());
app.listen(3000);
console.log('Server successfully listen at port 3000 ......');
