"statesearch" looks up org/state combos and opens their Wiki pages if the text of the articles
includes a mention of the state. "wiki2" looks up donor last name/org combos and opens
pages if the text of the articles includes a mention of the last name. Both programs also
try various substitutions if the initial search fails (e.g. "corporation" for "corp).

Here is the SQL code that generates the list for wiki2:

```SQL 
select lastname, orgname, sum(amount) as total
from margeindivs..indivs_all a
left join marge..cmtes_all b
on a.recipid = b.cmteid and a.cycle = b.cycle
where a.realcode like 'y%' and (b.primcode not like 'z4%' or b.primcode is null)
and orgname <> '' and (a.source = '' or a.source is null or a.source = '     ')
and lastname is not null and lastname <> ''
group by lastname, orgname
having sum(amount) > 9999
order by total desc
```

And here is the SQL code for statesearch: