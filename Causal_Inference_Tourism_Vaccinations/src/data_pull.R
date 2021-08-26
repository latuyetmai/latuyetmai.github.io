load_attractions <- function() { 
  attractions_raw <- read_csv('../data/attractions.csv')
  
  attractions <- attractions_raw %>% 
    select(Attraction, FIPS)
  
  return(attractions)

}

load_mobility <- function() { 
  mobility_raw <- read_csv('../data/jun21_mobility.csv')
  
  mobility <- mobility_raw %>% 
    select(-X1) %>% 
    mutate(mobility = jun21_mobility + 1)
  
  mobility$county_fips_code <- as.numeric(mobility$county_fips_code)
  
  return(mobility)
  
}

load_popdensity <- function() {
  
  census <- read.csv('../data/co-est2019-alldata.csv') %>% select(STATE,COUNTY,CTYNAME,POPESTIMATE2019)
  
  census <- census %>% mutate(COUNTY = str_pad(COUNTY, 3, pad="0")) %>% mutate(FIPS = as.numeric(paste(STATE,COUNTY,sep="")))
  
  landarea <- read.csv('../data/county_land_area.csv', header=TRUE) 
  
  census <- census %>% inner_join(landarea) %>% drop_na()
  
  census <- census %>% mutate(pop_density = POPESTIMATE2019 / as.numeric(gsub(",","",LAND.AREA..Square.Miles.)))
  
  census <- census %>% select(c(FIPS,pop_density))
  
  return(census)
  
}


load_election <- function() {

  electionv2 <- read.csv('../data/election_results.csv')
  
    electionv2$county_fips[electionv2$county_fips < 10000 & electionv2$county_fips %/% 100 == 29] <- electionv2$county_fips[electionv2$county_fips < 10000 & electionv2$county_fips %/% 100 == 29] - 900
    
    electionv2 <- electionv2 %>% select(c(county_fips, per_dem)) %>% rename('FIPS' = 'county_fips', 'pct_dem' = 'per_dem')
  
  return(electionv2)

}

load_urban <- function() {
  
  urb_rur <- read.csv("../data/urban_rural.csv", header=TRUE) %>% drop_na()
  
  urb_rur <- urb_rur %>% select(c(FIPS, urb_rur, RUCC_2013))
  
  urb_rur <- urb_rur %>% mutate(urb_rur = 1 - urb_rur, urban_index = (9 - RUCC_2013)/8)
  
  urb_rur <- urb_rur %>% select(c(FIPS, urban_index))
  
  return(urb_rur)
  
}


load_education <- function() { 
  education <- read.csv('../data/education.csv', header=TRUE) %>% drop_na()
  
  education <- education %>% 
    mutate(
      'some_college' = Percent.of.adults.completing.some.college.or.associate.s.degree..2015.19 + 
             Percent.of.adults.with.a.bachelor.s.degree.or.higher..2015.19) %>% 
    select(c(FIPS.Code, some_college)) %>% 
    rename('FIPS' = 'FIPS.Code') %>% 
    mutate(some_college = some_college/100)
  
  return(education)
  
}

load_clean_vacc <- function() { 
  vaccinations_by_fips <- read.socrata("https://data.cdc.gov/resource/8xkx-amqh.csv?$select=Recip_County, Recip_State, date, fips, series_complete_pop_pct, series_complete_yes&$where=fips in('01003','02020','04005','05051','06075','08069','09011','10005','12086','13121','15003','16001','17031','18097','19113','20173','21111','22071','23007','24003','25025','26163','27053','28047','29510','30031','31055','32003','33009','34001','35001','36061','37021','38017','39035','40109','41051','42101','44007','45019','46099','47157','48029','49035','50023','51095','53033','54039','55021','56029') AND date_extract_m(date)=6")
  
  vaccination_rates <- aggregate(vaccinations_by_fips[, 5:6], list(vaccinations_by_fips$fips, vaccinations_by_fips$Recip_State, vaccinations_by_fips$Recip_County), mean) %>% rename(county_fips_code=Group.1, state=Group.2, county=Group.3)
  
  vaccination_rates$county_fips_code <- as.character(vaccination_rates$county_fips_code)
  
  vaccination <- vaccination_rates %>% 
    select(-state,-county) %>% 
    rename(
      vaccination_rate = series_complete_pop_pct,
      vaccination_completion = series_complete_yes
    )
  
  vaccination$county_fips_code <- as.numeric(vaccination$county_fips_code)
  vaccination$vaccination_rate <- round(vaccination$vaccination_rate/100, 2)
  
  # Manually adding data points from the Bexar/Honolulu County websites (avg of June 1 and June 30, 2021)
  
  vaccination$vaccination_completion[vaccination$county_fips_code == 48029] = 914050
  vaccination$vaccination_rate[vaccination$county_fips_code == 48029] = 0.63
  
  vaccination$vaccination_completion[vaccination$county_fips_code == 15003] = 573217
  vaccination$vaccination_rate[vaccination$county_fips_code == 15003] = 573217/984819
  
  return(vaccination)
  
}

load_clean_income <- function(){
  income_raw <- read_csv('../data/income.csv')
  
  colnames(income_raw) <- gsub(" ", "_", colnames(income_raw))
  
  income <- income_raw %>%
    filter(Area_Type == "County", Ownership == "Total Covered") %>% 
    select(Area_Code, Annual_Average_Pay) %>% 
    rename(
      FIPS = Area_Code,
      annual_income = Annual_Average_Pay
    ) %>% 
    mutate(income_index = round(annual_income/64013,2))
  
  income$FIPS <- as.numeric(income$FIPS)
  
  return(income)
}

load_clean_political <- function(){
  election_raw <- read_csv('../data/president_county_candidate.csv')
  
  winner <- election_raw %>%
    filter(won == TRUE) %>%
    rename(
      winner = candidate,
      winner_votes = total_votes,
      winner_party = party)
  
  political_leaning <- election_raw %>% 
    group_by(state, county) %>% 
    summarise(all_votes = sum(total_votes)) %>% 
    inner_join(winner) %>%
    mutate(won_pct = winner_votes/all_votes) %>%
    mutate(
      lean_party = case_when(
        winner_party == "REP" & won_pct >= 0.5 ~ "REP",
        winner_party == "DEM" & won_pct >= 0.5 ~ "DEM",
        TRUE ~ "Swing"
      )
    )
  
  party <- political_leaning %>% 
    select(state, county, winner_party, won_pct, lean_party)
  
  return(political_leaning)
}

clean_merge <- function(){
  attractions <- load_attractions()
  education <- load_education()
  mobility <- load_mobility()
  election <- load_election()
  urban <- load_urban()
  party <- load_clean_political()
  vaccination <- load_clean_vacc()
  income <- load_clean_income()
  pop_density <- load_popdensity()
  
  merge_data <- attractions %>%
    right_join(mobility, by = c("FIPS" = "county_fips_code")) %>% 
    left_join(vaccination, by = c("FIPS" = "county_fips_code")) %>% 
    left_join(education) %>%
    left_join(income) %>%
    left_join(urban) %>%
    left_join(election) %>%
    left_join(party, by = c("state","county")) %>%
    left_join(pop_density) %>%
    filter(vaccination_rate > 0) %>% 
    mutate(
      DEM = if_else(lean_party == "DEM", 1 , 0),
      REP = if_else(lean_party == "REP", 1 , 0),
    )
  
  merge_data$lean_party <- as.factor(merge_data$lean_party)
  
  return(merge_data)
}
