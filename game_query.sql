USE game_analytics;

Select count(*) from categories;
Select count(*) from competitions;
Select count(*) from competitor_rankings;
Select count(*) from competitors;
Select count(*) from complexes;
Select count(*) from venues;

Select * from categories;
Select * from competitions;
Select * from competitor_rankings;
Select * from competitors;
Select * from complexes;
Select * from venues;

# 1) List all competitions along with their category name
Select cat.category_name, comp.competition_name
from categories as cat
join competitions as comp on cat.category_id = comp.category_id;

# 2) Count the number of competitions in each category
Select cat.category_name, count(comp.competition_id) as No_of_competition
from categories as cat
join competitions as comp on cat.category_id = comp.category_id
group by cat.category_name
order by No_of_competition desc;

# 3) Find all competitions of type 'doubles'
Select competition_id, competition_name, type
from competitions
where type = "doubles";

# 4) Get competitions that belong to a specific category (e.g., ITF Men)
Select cat.category_name, comp.competition_name
from categories as cat
join competitions as comp on cat.category_id = comp.category_id
where category_name = "ITF Men";

# 5) Identify parent competitions and their sub-competitions
Select parent.competition_id  as parent_competition_id,
parent.competition_name as parent_competition_name,
child.competition_id as sub_competition_id,
child.competition_name as sub_competition_name,
child.type, child.gender
FROM competitions as child
JOIN competitions as parent ON child.parent_id = parent.competition_id
ORDER BY parent.competition_name, child.competition_name;

# 6) Analyze the distribution of competition types by category
Select c.category_name, comp.type AS competition_type,
COUNT(*) AS total_competitions
FROM competitions comp
JOIN categories c ON comp.category_id = c.category_id
GROUP BY c.category_name, comp.type
ORDER BY c.category_name, total_competitions DESC;

# 7) List all competitions with no parent (top-level competitions)
Select competition_id, competition_name, type, gender,
level, category_id
FROM competitions
WHERE parent_id IS NULL
ORDER BY competition_name;


-------------------------------------------------------------------------------------------------------

# 1) List all venues along with their associated complex name
Select ven.venue_name, compl.complex_name
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id;


# 2) Count the number of venues in each complex
Select compl.complex_id, compl.complex_name, count(ven.venue_id) as no_of_venue
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id
group by compl.complex_id, compl.complex_name
order by no_of_venue desc;


# 3) Get details of venues in a specific country (e.g., Chile)
Select ven.venue_id, ven.venue_name
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id
where country_name = "Chile";


# 4) Identify all venues and their timezones
Select ven.venue_id, ven.venue_name, timezone
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id;


# 5) Find complexes that have more than one venue
Select compl.complex_id, compl.complex_name, count(ven.venue_id) as no_of_venue
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id
group by compl.complex_id, compl.complex_name
having count(ven.venue_id) >1
order by no_of_venue desc;

# 6) List venues grouped by country
Select ven.country_name, count(ven.venue_id) as no_of_venue
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id
group by ven.country_name;


# 7) Find all venues for a specific complex (e.g., Nacional)
Select ven.venue_id, ven.venue_name
from complexes as compl
join venues as ven on compl.complex_id = ven.complex_id
where compl.complex_name = "Nacional";



------------------------------------------------------------------------------


# 1) Get all competitors with their rank and points.
Select compt.competitor_id, compt.name, comptrnk.ranking, comptrnk.points
from competitors as compt
join competitor_rankings as comptrnk on compt.competitor_id = comptrnk.competitor_id
order by comptrnk.ranking asc;


# 2) Find competitors ranked in the top 5
Select compt.competitor_id, compt.name, comptrnk.ranking, comptrnk.points
from competitors as compt
join competitor_rankings as comptrnk on compt.competitor_id = comptrnk.competitor_id
order by comptrnk.ranking asc
limit 5;


# 3) List competitors with no rank movement (stable rank)
Select compt.competitor_id, compt.name, comptrnk.ranking, comptrnk.movement
from competitors as compt
join competitor_rankings as comptrnk on compt.competitor_id = comptrnk.competitor_id
where comptrnk.movement = 0;

# 4) Get the total points of competitors from a specific country (e.g., Croatia)
with cte1 as (Select compt.country, sum(points) as total_points
from competitors as compt
join competitor_rankings as comptrnk on compt.competitor_id = comptrnk.competitor_id
group by compt.country)

select country, total_points
from cte1
where country = "Croatia";


# 5) Count the number of competitors per country
Select compt.country, count(compt.competitor_id) as no_of_competitors
from competitors as compt
join competitor_rankings as comptrnk on compt.competitor_id = comptrnk.competitor_id
group by compt.country
order by no_of_competitors desc;


# 6) Find competitors with the highest points in the current week
Select compt.competitor_id, compt.name, max(comptrnk.points) as max_points
FROM competitors AS compt
JOIN competitor_rankings AS comptrnk 
ON compt.competitor_id = comptrnk.competitor_id
group by compt.competitor_id, compt.name
order by max_points desc
limit 1;

