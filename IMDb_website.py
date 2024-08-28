{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "c664f60a",
   "metadata": {},
   "source": [
    "### IMDB Dataset of top 500 movies and tv shows"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bb2b01d5",
   "metadata": {},
   "source": [
    "#### Importing all required libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "bf9b5ef8",
   "metadata": {},
   "outputs": [],
   "source": [
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "import re\n",
    "import time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "0fe678d3",
   "metadata": {},
   "outputs": [],
   "source": [
    "imdb = pd.read_csv(\"imdb.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "b95d4a20",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Title</th>\n",
       "      <th>Released_Year</th>\n",
       "      <th>certificate</th>\n",
       "      <th>RunTime</th>\n",
       "      <th>Genre</th>\n",
       "      <th>Ratings</th>\n",
       "      <th>Overview</th>\n",
       "      <th>MetaScore</th>\n",
       "      <th>Director</th>\n",
       "      <th>Star1</th>\n",
       "      <th>Star2</th>\n",
       "      <th>Star3</th>\n",
       "      <th>Star4</th>\n",
       "      <th>Votes</th>\n",
       "      <th>Gross(M)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Citizen Kane</td>\n",
       "      <td>1941</td>\n",
       "      <td>UA</td>\n",
       "      <td>119</td>\n",
       "      <td>Drama, Mystery</td>\n",
       "      <td>8.3</td>\n",
       "      <td>Following the death of publishing tycoon Charl...</td>\n",
       "      <td>100</td>\n",
       "      <td>Orson Welles</td>\n",
       "      <td>Orson Welles</td>\n",
       "      <td>Joseph Cotten</td>\n",
       "      <td>Dorothy Comingore</td>\n",
       "      <td>Agnes Moorehead</td>\n",
       "      <td>458535</td>\n",
       "      <td>1.59</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>The Godfather</td>\n",
       "      <td>1972</td>\n",
       "      <td>A</td>\n",
       "      <td>175</td>\n",
       "      <td>Crime, Drama</td>\n",
       "      <td>9.2</td>\n",
       "      <td>Don Vito Corleone, head of a mafia family, dec...</td>\n",
       "      <td>100</td>\n",
       "      <td>Francis Ford Coppola</td>\n",
       "      <td>Marlon Brando</td>\n",
       "      <td>Al Pacino</td>\n",
       "      <td>James Caan</td>\n",
       "      <td>Diane Keaton</td>\n",
       "      <td>1964</td>\n",
       "      <td>134.97</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>The Wizard of Oz</td>\n",
       "      <td>1939</td>\n",
       "      <td>U</td>\n",
       "      <td>102</td>\n",
       "      <td>Adventure, Family, Fantasy</td>\n",
       "      <td>8.1</td>\n",
       "      <td>Young Dorothy Gale and her dog Toto are swept ...</td>\n",
       "      <td>92</td>\n",
       "      <td>Victor Fleming,</td>\n",
       "      <td>Judy Garland</td>\n",
       "      <td>Frank Morgan</td>\n",
       "      <td>Ray Bolger</td>\n",
       "      <td>Bert Lahr</td>\n",
       "      <td>419203</td>\n",
       "      <td>2.08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>The Shawshank Redemption</td>\n",
       "      <td>1994</td>\n",
       "      <td>A</td>\n",
       "      <td>142</td>\n",
       "      <td>Drama</td>\n",
       "      <td>9.3</td>\n",
       "      <td>Over the course of several years, two convicts...</td>\n",
       "      <td>82</td>\n",
       "      <td>Frank Darabont</td>\n",
       "      <td>Tim Robbins</td>\n",
       "      <td>Morgan Freeman</td>\n",
       "      <td>Bob Gunton</td>\n",
       "      <td>William Sadler</td>\n",
       "      <td>2819</td>\n",
       "      <td>28.34</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Pulp Fiction</td>\n",
       "      <td>1994</td>\n",
       "      <td>A</td>\n",
       "      <td>154</td>\n",
       "      <td>Crime, Drama</td>\n",
       "      <td>8.9</td>\n",
       "      <td>The lives of two mob hitmen, a boxer, a gangst...</td>\n",
       "      <td>95</td>\n",
       "      <td>Quentin Tarantino</td>\n",
       "      <td>John Travolta</td>\n",
       "      <td>Uma Thurman</td>\n",
       "      <td>Samuel L. Jackson</td>\n",
       "      <td>Bruce Willis</td>\n",
       "      <td>2161</td>\n",
       "      <td>107.93</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>512</th>\n",
       "      <td>From Here to Eternity</td>\n",
       "      <td>1953</td>\n",
       "      <td>UA</td>\n",
       "      <td>118</td>\n",
       "      <td>Drama, Romance, War</td>\n",
       "      <td>7.6</td>\n",
       "      <td>At a U.S. Army base in 1941 Hawaii, a private ...</td>\n",
       "      <td>85</td>\n",
       "      <td>Fred Zinnemann</td>\n",
       "      <td>Burt Lancaster</td>\n",
       "      <td>Montgomery Clift</td>\n",
       "      <td>Deborah Kerr</td>\n",
       "      <td>Donna Reed</td>\n",
       "      <td>49929</td>\n",
       "      <td>30.50</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>513</th>\n",
       "      <td>Walk the Line</td>\n",
       "      <td>2005</td>\n",
       "      <td>U</td>\n",
       "      <td>136</td>\n",
       "      <td>Biography, Drama, Music</td>\n",
       "      <td>7.8</td>\n",
       "      <td>A chronicle of country music legend Johnny Cas...</td>\n",
       "      <td>72</td>\n",
       "      <td>James Mangold</td>\n",
       "      <td>Joaquin Phoenix</td>\n",
       "      <td>Reese Witherspoon</td>\n",
       "      <td>Ginnifer Goodwin</td>\n",
       "      <td>Robert Patrick</td>\n",
       "      <td>261587</td>\n",
       "      <td>119.52</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>514</th>\n",
       "      <td>The Last Emperor</td>\n",
       "      <td>1987</td>\n",
       "      <td>U</td>\n",
       "      <td>163</td>\n",
       "      <td>Biography, Drama, History</td>\n",
       "      <td>7.7</td>\n",
       "      <td>Bernardo Bertolucci's Oscar-winning dramatisat...</td>\n",
       "      <td>76</td>\n",
       "      <td>Bernardo Bertolucci</td>\n",
       "      <td>John Lone</td>\n",
       "      <td>Joan Chen</td>\n",
       "      <td>Peter O'Toole</td>\n",
       "      <td>Ruocheng Ying</td>\n",
       "      <td>109219</td>\n",
       "      <td>43.98</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>515</th>\n",
       "      <td>Mutiny on the Bounty</td>\n",
       "      <td>1935</td>\n",
       "      <td>U</td>\n",
       "      <td>132</td>\n",
       "      <td>Adventure, Biography, Drama</td>\n",
       "      <td>7.6</td>\n",
       "      <td>First mate Fletcher Christian leads a revolt a...</td>\n",
       "      <td>87</td>\n",
       "      <td>Frank Lloyd</td>\n",
       "      <td>Charles Laughton</td>\n",
       "      <td>Clark Gable</td>\n",
       "      <td>Franchot Tone</td>\n",
       "      <td>Herbert Mundin</td>\n",
       "      <td>24381</td>\n",
       "      <td>87.65</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>516</th>\n",
       "      <td>The Longest Day</td>\n",
       "      <td>1962</td>\n",
       "      <td>U</td>\n",
       "      <td>178</td>\n",
       "      <td>Action, Drama, History</td>\n",
       "      <td>7.7</td>\n",
       "      <td>The events of D-Day, told on a grand scale fro...</td>\n",
       "      <td>75</td>\n",
       "      <td>Ken Annakin,</td>\n",
       "      <td>John Wayne</td>\n",
       "      <td>Robert Ryan</td>\n",
       "      <td>Richard Burton</td>\n",
       "      <td>Henry Fonda</td>\n",
       "      <td>58278</td>\n",
       "      <td>39.10</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>517 rows × 15 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                        Title  Released_Year certificate  RunTime  \\\n",
       "0                Citizen Kane           1941          UA      119   \n",
       "1               The Godfather           1972           A      175   \n",
       "2            The Wizard of Oz           1939           U      102   \n",
       "3    The Shawshank Redemption           1994           A      142   \n",
       "4                Pulp Fiction           1994           A      154   \n",
       "..                        ...            ...         ...      ...   \n",
       "512     From Here to Eternity           1953          UA      118   \n",
       "513             Walk the Line           2005           U      136   \n",
       "514          The Last Emperor           1987           U      163   \n",
       "515      Mutiny on the Bounty           1935           U      132   \n",
       "516           The Longest Day           1962           U      178   \n",
       "\n",
       "                                       Genre  Ratings  \\\n",
       "0                 Drama, Mystery                  8.3   \n",
       "1                   Crime, Drama                  9.2   \n",
       "2     Adventure, Family, Fantasy                  8.1   \n",
       "3                          Drama                  9.3   \n",
       "4                   Crime, Drama                  8.9   \n",
       "..                                       ...      ...   \n",
       "512          Drama, Romance, War                  7.6   \n",
       "513      Biography, Drama, Music                  7.8   \n",
       "514    Biography, Drama, History                  7.7   \n",
       "515  Adventure, Biography, Drama                  7.6   \n",
       "516       Action, Drama, History                  7.7   \n",
       "\n",
       "                                              Overview  MetaScore  \\\n",
       "0    Following the death of publishing tycoon Charl...        100   \n",
       "1    Don Vito Corleone, head of a mafia family, dec...        100   \n",
       "2    Young Dorothy Gale and her dog Toto are swept ...         92   \n",
       "3    Over the course of several years, two convicts...         82   \n",
       "4    The lives of two mob hitmen, a boxer, a gangst...         95   \n",
       "..                                                 ...        ...   \n",
       "512  At a U.S. Army base in 1941 Hawaii, a private ...         85   \n",
       "513  A chronicle of country music legend Johnny Cas...         72   \n",
       "514  Bernardo Bertolucci's Oscar-winning dramatisat...         76   \n",
       "515  First mate Fletcher Christian leads a revolt a...         87   \n",
       "516  The events of D-Day, told on a grand scale fro...         75   \n",
       "\n",
       "                 Director             Star1               Star2  \\\n",
       "0            Orson Welles      Orson Welles       Joseph Cotten   \n",
       "1    Francis Ford Coppola     Marlon Brando           Al Pacino   \n",
       "2        Victor Fleming,       Judy Garland        Frank Morgan   \n",
       "3          Frank Darabont       Tim Robbins      Morgan Freeman   \n",
       "4       Quentin Tarantino     John Travolta         Uma Thurman   \n",
       "..                    ...               ...                 ...   \n",
       "512        Fred Zinnemann    Burt Lancaster    Montgomery Clift   \n",
       "513         James Mangold   Joaquin Phoenix   Reese Witherspoon   \n",
       "514   Bernardo Bertolucci         John Lone           Joan Chen   \n",
       "515           Frank Lloyd  Charles Laughton         Clark Gable   \n",
       "516         Ken Annakin,         John Wayne         Robert Ryan   \n",
       "\n",
       "                  Star3             Star4   Votes  Gross(M)  \n",
       "0     Dorothy Comingore   Agnes Moorehead  458535      1.59  \n",
       "1            James Caan      Diane Keaton    1964    134.97  \n",
       "2            Ray Bolger         Bert Lahr  419203      2.08  \n",
       "3            Bob Gunton    William Sadler    2819     28.34  \n",
       "4     Samuel L. Jackson      Bruce Willis    2161    107.93  \n",
       "..                  ...               ...     ...       ...  \n",
       "512        Deborah Kerr        Donna Reed   49929     30.50  \n",
       "513    Ginnifer Goodwin    Robert Patrick  261587    119.52  \n",
       "514       Peter O'Toole     Ruocheng Ying  109219     43.98  \n",
       "515       Franchot Tone    Herbert Mundin   24381     87.65  \n",
       "516      Richard Burton       Henry Fonda   58278     39.10  \n",
       "\n",
       "[517 rows x 15 columns]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f1a519a4",
   "metadata": {},
   "source": [
    "#### Number of Null values"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "id": "bad80eee",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Title            0\n",
       "Released_Year    0\n",
       "certificate      0\n",
       "RunTime          0\n",
       "Genre            0\n",
       "Ratings          0\n",
       "Overview         0\n",
       "MetaScore        0\n",
       "Director         0\n",
       "Star1            0\n",
       "Star2            0\n",
       "Star3            0\n",
       "Star4            0\n",
       "Votes            0\n",
       "Gross(M)         0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 72,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.isnull().sum() # check for null values , there should not be any null values"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cca4c915",
   "metadata": {},
   "source": [
    "### Type of Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "id": "88d1f4a3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Title             object\n",
       "Released_Year      int64\n",
       "certificate       object\n",
       "RunTime            int64\n",
       "Genre             object\n",
       "Ratings          float64\n",
       "Overview          object\n",
       "MetaScore          int64\n",
       "Director          object\n",
       "Star1             object\n",
       "Star2             object\n",
       "Star3             object\n",
       "Star4             object\n",
       "Votes              int64\n",
       "Gross(M)         float64\n",
       "dtype: object"
      ]
     },
     "execution_count": 73,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.dtypes # type of data "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e22dd04d",
   "metadata": {},
   "source": [
    "## Shape of the Database"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "d817067c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The shape of the dataset is: 517 rows and 15 columns\n"
     ]
    }
   ],
   "source": [
    "print(\"The shape of the dataset is: {} rows and {} columns\".format(imdb.shape[0], imdb.shape[1]))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ed738f2f",
   "metadata": {},
   "source": [
    "## Quick View of Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "id": "d46f4210",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Title</th>\n",
       "      <th>Released_Year</th>\n",
       "      <th>certificate</th>\n",
       "      <th>RunTime</th>\n",
       "      <th>Genre</th>\n",
       "      <th>Ratings</th>\n",
       "      <th>Overview</th>\n",
       "      <th>MetaScore</th>\n",
       "      <th>Director</th>\n",
       "      <th>Star1</th>\n",
       "      <th>Star2</th>\n",
       "      <th>Star3</th>\n",
       "      <th>Star4</th>\n",
       "      <th>Votes</th>\n",
       "      <th>Gross(M)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Citizen Kane</td>\n",
       "      <td>1941</td>\n",
       "      <td>UA</td>\n",
       "      <td>119</td>\n",
       "      <td>Drama, Mystery</td>\n",
       "      <td>8.3</td>\n",
       "      <td>Following the death of publishing tycoon Charl...</td>\n",
       "      <td>100</td>\n",
       "      <td>Orson Welles</td>\n",
       "      <td>Orson Welles</td>\n",
       "      <td>Joseph Cotten</td>\n",
       "      <td>Dorothy Comingore</td>\n",
       "      <td>Agnes Moorehead</td>\n",
       "      <td>458535</td>\n",
       "      <td>1.59</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>The Godfather</td>\n",
       "      <td>1972</td>\n",
       "      <td>A</td>\n",
       "      <td>175</td>\n",
       "      <td>Crime, Drama</td>\n",
       "      <td>9.2</td>\n",
       "      <td>Don Vito Corleone, head of a mafia family, dec...</td>\n",
       "      <td>100</td>\n",
       "      <td>Francis Ford Coppola</td>\n",
       "      <td>Marlon Brando</td>\n",
       "      <td>Al Pacino</td>\n",
       "      <td>James Caan</td>\n",
       "      <td>Diane Keaton</td>\n",
       "      <td>1964</td>\n",
       "      <td>134.97</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>The Wizard of Oz</td>\n",
       "      <td>1939</td>\n",
       "      <td>U</td>\n",
       "      <td>102</td>\n",
       "      <td>Adventure, Family, Fantasy</td>\n",
       "      <td>8.1</td>\n",
       "      <td>Young Dorothy Gale and her dog Toto are swept ...</td>\n",
       "      <td>92</td>\n",
       "      <td>Victor Fleming,</td>\n",
       "      <td>Judy Garland</td>\n",
       "      <td>Frank Morgan</td>\n",
       "      <td>Ray Bolger</td>\n",
       "      <td>Bert Lahr</td>\n",
       "      <td>419203</td>\n",
       "      <td>2.08</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>The Shawshank Redemption</td>\n",
       "      <td>1994</td>\n",
       "      <td>A</td>\n",
       "      <td>142</td>\n",
       "      <td>Drama</td>\n",
       "      <td>9.3</td>\n",
       "      <td>Over the course of several years, two convicts...</td>\n",
       "      <td>82</td>\n",
       "      <td>Frank Darabont</td>\n",
       "      <td>Tim Robbins</td>\n",
       "      <td>Morgan Freeman</td>\n",
       "      <td>Bob Gunton</td>\n",
       "      <td>William Sadler</td>\n",
       "      <td>2819</td>\n",
       "      <td>28.34</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Pulp Fiction</td>\n",
       "      <td>1994</td>\n",
       "      <td>A</td>\n",
       "      <td>154</td>\n",
       "      <td>Crime, Drama</td>\n",
       "      <td>8.9</td>\n",
       "      <td>The lives of two mob hitmen, a boxer, a gangst...</td>\n",
       "      <td>95</td>\n",
       "      <td>Quentin Tarantino</td>\n",
       "      <td>John Travolta</td>\n",
       "      <td>Uma Thurman</td>\n",
       "      <td>Samuel L. Jackson</td>\n",
       "      <td>Bruce Willis</td>\n",
       "      <td>2161</td>\n",
       "      <td>107.93</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                      Title  Released_Year certificate  RunTime  \\\n",
       "0              Citizen Kane           1941          UA      119   \n",
       "1             The Godfather           1972           A      175   \n",
       "2          The Wizard of Oz           1939           U      102   \n",
       "3  The Shawshank Redemption           1994           A      142   \n",
       "4              Pulp Fiction           1994           A      154   \n",
       "\n",
       "                                    Genre  Ratings  \\\n",
       "0              Drama, Mystery                  8.3   \n",
       "1                Crime, Drama                  9.2   \n",
       "2  Adventure, Family, Fantasy                  8.1   \n",
       "3                       Drama                  9.3   \n",
       "4                Crime, Drama                  8.9   \n",
       "\n",
       "                                            Overview  MetaScore  \\\n",
       "0  Following the death of publishing tycoon Charl...        100   \n",
       "1  Don Vito Corleone, head of a mafia family, dec...        100   \n",
       "2  Young Dorothy Gale and her dog Toto are swept ...         92   \n",
       "3  Over the course of several years, two convicts...         82   \n",
       "4  The lives of two mob hitmen, a boxer, a gangst...         95   \n",
       "\n",
       "               Director          Star1            Star2               Star3  \\\n",
       "0          Orson Welles   Orson Welles    Joseph Cotten   Dorothy Comingore   \n",
       "1  Francis Ford Coppola  Marlon Brando        Al Pacino          James Caan   \n",
       "2      Victor Fleming,    Judy Garland     Frank Morgan          Ray Bolger   \n",
       "3        Frank Darabont    Tim Robbins   Morgan Freeman          Bob Gunton   \n",
       "4     Quentin Tarantino  John Travolta      Uma Thurman   Samuel L. Jackson   \n",
       "\n",
       "              Star4   Votes  Gross(M)  \n",
       "0   Agnes Moorehead  458535      1.59  \n",
       "1      Diane Keaton    1964    134.97  \n",
       "2         Bert Lahr  419203      2.08  \n",
       "3    William Sadler    2819     28.34  \n",
       "4      Bruce Willis    2161    107.93  "
      ]
     },
     "execution_count": 74,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "id": "734e1f67",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Title</th>\n",
       "      <th>Released_Year</th>\n",
       "      <th>certificate</th>\n",
       "      <th>RunTime</th>\n",
       "      <th>Genre</th>\n",
       "      <th>Ratings</th>\n",
       "      <th>Overview</th>\n",
       "      <th>MetaScore</th>\n",
       "      <th>Director</th>\n",
       "      <th>Star1</th>\n",
       "      <th>Star2</th>\n",
       "      <th>Star3</th>\n",
       "      <th>Star4</th>\n",
       "      <th>Votes</th>\n",
       "      <th>Gross(M)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>512</th>\n",
       "      <td>From Here to Eternity</td>\n",
       "      <td>1953</td>\n",
       "      <td>UA</td>\n",
       "      <td>118</td>\n",
       "      <td>Drama, Romance, War</td>\n",
       "      <td>7.6</td>\n",
       "      <td>At a U.S. Army base in 1941 Hawaii, a private ...</td>\n",
       "      <td>85</td>\n",
       "      <td>Fred Zinnemann</td>\n",
       "      <td>Burt Lancaster</td>\n",
       "      <td>Montgomery Clift</td>\n",
       "      <td>Deborah Kerr</td>\n",
       "      <td>Donna Reed</td>\n",
       "      <td>49929</td>\n",
       "      <td>30.50</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>513</th>\n",
       "      <td>Walk the Line</td>\n",
       "      <td>2005</td>\n",
       "      <td>U</td>\n",
       "      <td>136</td>\n",
       "      <td>Biography, Drama, Music</td>\n",
       "      <td>7.8</td>\n",
       "      <td>A chronicle of country music legend Johnny Cas...</td>\n",
       "      <td>72</td>\n",
       "      <td>James Mangold</td>\n",
       "      <td>Joaquin Phoenix</td>\n",
       "      <td>Reese Witherspoon</td>\n",
       "      <td>Ginnifer Goodwin</td>\n",
       "      <td>Robert Patrick</td>\n",
       "      <td>261587</td>\n",
       "      <td>119.52</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>514</th>\n",
       "      <td>The Last Emperor</td>\n",
       "      <td>1987</td>\n",
       "      <td>U</td>\n",
       "      <td>163</td>\n",
       "      <td>Biography, Drama, History</td>\n",
       "      <td>7.7</td>\n",
       "      <td>Bernardo Bertolucci's Oscar-winning dramatisat...</td>\n",
       "      <td>76</td>\n",
       "      <td>Bernardo Bertolucci</td>\n",
       "      <td>John Lone</td>\n",
       "      <td>Joan Chen</td>\n",
       "      <td>Peter O'Toole</td>\n",
       "      <td>Ruocheng Ying</td>\n",
       "      <td>109219</td>\n",
       "      <td>43.98</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>515</th>\n",
       "      <td>Mutiny on the Bounty</td>\n",
       "      <td>1935</td>\n",
       "      <td>U</td>\n",
       "      <td>132</td>\n",
       "      <td>Adventure, Biography, Drama</td>\n",
       "      <td>7.6</td>\n",
       "      <td>First mate Fletcher Christian leads a revolt a...</td>\n",
       "      <td>87</td>\n",
       "      <td>Frank Lloyd</td>\n",
       "      <td>Charles Laughton</td>\n",
       "      <td>Clark Gable</td>\n",
       "      <td>Franchot Tone</td>\n",
       "      <td>Herbert Mundin</td>\n",
       "      <td>24381</td>\n",
       "      <td>87.65</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>516</th>\n",
       "      <td>The Longest Day</td>\n",
       "      <td>1962</td>\n",
       "      <td>U</td>\n",
       "      <td>178</td>\n",
       "      <td>Action, Drama, History</td>\n",
       "      <td>7.7</td>\n",
       "      <td>The events of D-Day, told on a grand scale fro...</td>\n",
       "      <td>75</td>\n",
       "      <td>Ken Annakin,</td>\n",
       "      <td>John Wayne</td>\n",
       "      <td>Robert Ryan</td>\n",
       "      <td>Richard Burton</td>\n",
       "      <td>Henry Fonda</td>\n",
       "      <td>58278</td>\n",
       "      <td>39.10</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     Title  Released_Year certificate  RunTime  \\\n",
       "512  From Here to Eternity           1953          UA      118   \n",
       "513          Walk the Line           2005           U      136   \n",
       "514       The Last Emperor           1987           U      163   \n",
       "515   Mutiny on the Bounty           1935           U      132   \n",
       "516        The Longest Day           1962           U      178   \n",
       "\n",
       "                                       Genre  Ratings  \\\n",
       "512          Drama, Romance, War                  7.6   \n",
       "513      Biography, Drama, Music                  7.8   \n",
       "514    Biography, Drama, History                  7.7   \n",
       "515  Adventure, Biography, Drama                  7.6   \n",
       "516       Action, Drama, History                  7.7   \n",
       "\n",
       "                                              Overview  MetaScore  \\\n",
       "512  At a U.S. Army base in 1941 Hawaii, a private ...         85   \n",
       "513  A chronicle of country music legend Johnny Cas...         72   \n",
       "514  Bernardo Bertolucci's Oscar-winning dramatisat...         76   \n",
       "515  First mate Fletcher Christian leads a revolt a...         87   \n",
       "516  The events of D-Day, told on a grand scale fro...         75   \n",
       "\n",
       "                Director             Star1               Star2  \\\n",
       "512       Fred Zinnemann    Burt Lancaster    Montgomery Clift   \n",
       "513        James Mangold   Joaquin Phoenix   Reese Witherspoon   \n",
       "514  Bernardo Bertolucci         John Lone           Joan Chen   \n",
       "515          Frank Lloyd  Charles Laughton         Clark Gable   \n",
       "516        Ken Annakin,         John Wayne         Robert Ryan   \n",
       "\n",
       "                 Star3            Star4   Votes  Gross(M)  \n",
       "512       Deborah Kerr       Donna Reed   49929     30.50  \n",
       "513   Ginnifer Goodwin   Robert Patrick  261587    119.52  \n",
       "514      Peter O'Toole    Ruocheng Ying  109219     43.98  \n",
       "515      Franchot Tone   Herbert Mundin   24381     87.65  \n",
       "516     Richard Burton      Henry Fonda   58278     39.10  "
      ]
     },
     "execution_count": 75,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.tail()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ef44c9b1",
   "metadata": {},
   "source": [
    "### Finding correlation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 76,
   "id": "b178e74e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Released_Year</th>\n",
       "      <th>RunTime</th>\n",
       "      <th>Ratings</th>\n",
       "      <th>MetaScore</th>\n",
       "      <th>Votes</th>\n",
       "      <th>Gross(M)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Released_Year</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.145043</td>\n",
       "      <td>0.040116</td>\n",
       "      <td>-0.315399</td>\n",
       "      <td>0.382006</td>\n",
       "      <td>0.254868</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>RunTime</th>\n",
       "      <td>0.145043</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.258793</td>\n",
       "      <td>-0.057270</td>\n",
       "      <td>-0.023991</td>\n",
       "      <td>0.118852</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Ratings</th>\n",
       "      <td>0.040116</td>\n",
       "      <td>0.258793</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.041260</td>\n",
       "      <td>0.047909</td>\n",
       "      <td>0.096940</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>MetaScore</th>\n",
       "      <td>-0.315399</td>\n",
       "      <td>-0.057270</td>\n",
       "      <td>-0.041260</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.075901</td>\n",
       "      <td>-0.081244</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Votes</th>\n",
       "      <td>0.382006</td>\n",
       "      <td>-0.023991</td>\n",
       "      <td>0.047909</td>\n",
       "      <td>-0.075901</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.123955</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Gross(M)</th>\n",
       "      <td>0.254868</td>\n",
       "      <td>0.118852</td>\n",
       "      <td>0.096940</td>\n",
       "      <td>-0.081244</td>\n",
       "      <td>0.123955</td>\n",
       "      <td>1.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "               Released_Year   RunTime   Ratings  MetaScore     Votes  \\\n",
       "Released_Year       1.000000  0.145043  0.040116  -0.315399  0.382006   \n",
       "RunTime             0.145043  1.000000  0.258793  -0.057270 -0.023991   \n",
       "Ratings             0.040116  0.258793  1.000000  -0.041260  0.047909   \n",
       "MetaScore          -0.315399 -0.057270 -0.041260   1.000000 -0.075901   \n",
       "Votes               0.382006 -0.023991  0.047909  -0.075901  1.000000   \n",
       "Gross(M)            0.254868  0.118852  0.096940  -0.081244  0.123955   \n",
       "\n",
       "               Gross(M)  \n",
       "Released_Year  0.254868  \n",
       "RunTime        0.118852  \n",
       "Ratings        0.096940  \n",
       "MetaScore     -0.081244  \n",
       "Votes          0.123955  \n",
       "Gross(M)       1.000000  "
      ]
     },
     "execution_count": 76,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.corr()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 107,
   "id": "ea9af3d8",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.heatmap(imdb[[\"Released_Year\",\"RunTime\",\"Ratings\",\"MetaScore\",\"Votes\",\"Gross(M)\"]].corr(), annot=True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 77,
   "id": "4a60ee12",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x504 with 4 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "numerical_attributes = ['Ratings', 'MetaScore', 'Votes', 'Gross(M)']\n",
    "imdb[numerical_attributes].hist(figsize = (15, 7), color = 'pink', edgecolor = \"red\", layout = (2, 2));"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "65bb4fa9",
   "metadata": {},
   "source": [
    "### Insights\n",
    "\n",
    "1 . The above graph shows the values of Ratings ,  MetaScore , Votes , Gross(M) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 78,
   "id": "fe0f5092",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Title</th>\n",
       "      <th>certificate</th>\n",
       "      <th>Genre</th>\n",
       "      <th>Overview</th>\n",
       "      <th>Director</th>\n",
       "      <th>Star1</th>\n",
       "      <th>Star2</th>\n",
       "      <th>Star3</th>\n",
       "      <th>Star4</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "      <td>517</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>unique</th>\n",
       "      <td>513</td>\n",
       "      <td>15</td>\n",
       "      <td>164</td>\n",
       "      <td>517</td>\n",
       "      <td>302</td>\n",
       "      <td>368</td>\n",
       "      <td>460</td>\n",
       "      <td>476</td>\n",
       "      <td>492</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>top</th>\n",
       "      <td>Toy Story</td>\n",
       "      <td>U</td>\n",
       "      <td>Drama</td>\n",
       "      <td>Following the death of publishing tycoon Charl...</td>\n",
       "      <td>Steven Spielberg</td>\n",
       "      <td>Robert De Niro</td>\n",
       "      <td>Joseph Cotten</td>\n",
       "      <td>Carrie Fisher</td>\n",
       "      <td>Michael Caine</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>freq</th>\n",
       "      <td>3</td>\n",
       "      <td>155</td>\n",
       "      <td>43</td>\n",
       "      <td>1</td>\n",
       "      <td>11</td>\n",
       "      <td>7</td>\n",
       "      <td>3</td>\n",
       "      <td>4</td>\n",
       "      <td>3</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            Title certificate              Genre  \\\n",
       "count         517         517                517   \n",
       "unique        513          15                164   \n",
       "top     Toy Story           U  Drama               \n",
       "freq            3         155                 43   \n",
       "\n",
       "                                                 Overview          Director  \\\n",
       "count                                                 517               517   \n",
       "unique                                                517               302   \n",
       "top     Following the death of publishing tycoon Charl...  Steven Spielberg   \n",
       "freq                                                    1                11   \n",
       "\n",
       "                 Star1           Star2           Star3           Star4  \n",
       "count              517             517             517             517  \n",
       "unique             368             460             476             492  \n",
       "top     Robert De Niro   Joseph Cotten   Carrie Fisher   Michael Caine  \n",
       "freq                 7               3               4               3  "
      ]
     },
     "execution_count": 78,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.describe(include = ['O'])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a85092cc",
   "metadata": {},
   "source": [
    "### Insights\n",
    "\n",
    "1 . decribe(include = [\"O\"] ) shows the categorical column\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "id": "e0f5fad1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Released_Year</th>\n",
       "      <th>RunTime</th>\n",
       "      <th>Ratings</th>\n",
       "      <th>MetaScore</th>\n",
       "      <th>Votes</th>\n",
       "      <th>Gross(M)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>517.000000</td>\n",
       "      <td>517.000000</td>\n",
       "      <td>517.000000</td>\n",
       "      <td>517.000000</td>\n",
       "      <td>517.000000</td>\n",
       "      <td>517.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>1982.286267</td>\n",
       "      <td>122.622824</td>\n",
       "      <td>8.038491</td>\n",
       "      <td>83.558994</td>\n",
       "      <td>262700.473888</td>\n",
       "      <td>75.540542</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>25.593711</td>\n",
       "      <td>29.022828</td>\n",
       "      <td>0.316363</td>\n",
       "      <td>10.544980</td>\n",
       "      <td>264576.126395</td>\n",
       "      <td>106.819101</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>1916.000000</td>\n",
       "      <td>45.000000</td>\n",
       "      <td>7.100000</td>\n",
       "      <td>33.000000</td>\n",
       "      <td>1018.000000</td>\n",
       "      <td>0.010000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>1962.000000</td>\n",
       "      <td>102.000000</td>\n",
       "      <td>7.800000</td>\n",
       "      <td>77.000000</td>\n",
       "      <td>57527.000000</td>\n",
       "      <td>7.100000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>1987.000000</td>\n",
       "      <td>118.000000</td>\n",
       "      <td>8.000000</td>\n",
       "      <td>86.000000</td>\n",
       "      <td>166265.000000</td>\n",
       "      <td>44.020000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>2004.000000</td>\n",
       "      <td>138.000000</td>\n",
       "      <td>8.200000</td>\n",
       "      <td>91.000000</td>\n",
       "      <td>419429.000000</td>\n",
       "      <td>87.650000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>2018.000000</td>\n",
       "      <td>238.000000</td>\n",
       "      <td>9.300000</td>\n",
       "      <td>100.000000</td>\n",
       "      <td>968413.000000</td>\n",
       "      <td>936.660000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       Released_Year     RunTime     Ratings   MetaScore          Votes  \\\n",
       "count     517.000000  517.000000  517.000000  517.000000     517.000000   \n",
       "mean     1982.286267  122.622824    8.038491   83.558994  262700.473888   \n",
       "std        25.593711   29.022828    0.316363   10.544980  264576.126395   \n",
       "min      1916.000000   45.000000    7.100000   33.000000    1018.000000   \n",
       "25%      1962.000000  102.000000    7.800000   77.000000   57527.000000   \n",
       "50%      1987.000000  118.000000    8.000000   86.000000  166265.000000   \n",
       "75%      2004.000000  138.000000    8.200000   91.000000  419429.000000   \n",
       "max      2018.000000  238.000000    9.300000  100.000000  968413.000000   \n",
       "\n",
       "         Gross(M)  \n",
       "count  517.000000  \n",
       "mean    75.540542  \n",
       "std    106.819101  \n",
       "min      0.010000  \n",
       "25%      7.100000  \n",
       "50%     44.020000  \n",
       "75%     87.650000  \n",
       "max    936.660000  "
      ]
     },
     "execution_count": 79,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imdb.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "db4217b5",
   "metadata": {},
   "source": [
    "### Insights\n",
    "\n",
    "1. describe() shows all the statistical data "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "56b8040d",
   "metadata": {},
   "source": [
    "## Top voted movies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "id": "5f2d04cc",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_voted = imdb.sort_values(['Votes'], ascending = False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 81,
   "id": "10778b2b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x504 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(15,7))\n",
    "g=sns.barplot(x=top_voted['Title'][:7],y=top_voted['Votes'][:7], palette = 'hls')\n",
    "g.set_title(\"Top Voted Movies\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0530f73f",
   "metadata": {},
   "source": [
    "### Insights \n",
    "\n",
    "1. the above bargraph shows the top 7  most voted movies.\n",
    "2. A Beautiful Mind is the most voted movie. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5041b47d",
   "metadata": {},
   "source": [
    "## Top Rated movies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "227b7a2e",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_voted = imdb.sort_values(['Ratings'], ascending = False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "44ede2e7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(15,5))\n",
    "g=sns.barplot(x=top_voted['Title'][:7],y=top_voted['Ratings'][:7], palette = 'husl')\n",
    "g.set_title(\"IMDB Rating of top voted movies\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fa401d60",
   "metadata": {},
   "source": [
    "### Insights\n",
    "1 . the above bargraph shows the top 7 most Rated movies.\n",
    "\n",
    "2 . The Shawshank Redemption is the most voted movie."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c27c4b5d",
   "metadata": {},
   "source": [
    "## Gross of top rated movies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "acd5c065",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_voted = imdb.sort_values(['Ratings'], ascending = False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "6b7dd281",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(15,5))\n",
    "g=sns.barplot(x=top_voted['Title'][:7],y=top_voted['Gross(M)'][:7], palette = 'husl')\n",
    "g.set_title(\"Gross by top rated movies\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0f532e11",
   "metadata": {},
   "source": [
    "### Insights\n",
    "1 . the above bargraph shows the top 7 most  Gross Rated movies.\n",
    "\n",
    "2 . The Dark Knight is the most Gross Rated  movie."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "096ebe81",
   "metadata": {},
   "source": [
    "## Top movies by Gross\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "1fc48494",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1728x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "highest_earning = imdb.sort_values(['Gross(M)'], ascending = False)\n",
    "fig,axs=plt.subplots(figsize=(24,5))\n",
    "g=sns.barplot(x=highest_earning['Title'][:7],y=highest_earning['Gross(M)'][:7], palette = 'husl')\n",
    "g.set_title(\"Movies with highest Gross\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a83602fe",
   "metadata": {},
   "source": [
    "### Insights\n",
    "1 . the above bargraph shows the top 7 most Gross movies.\n",
    "\n",
    "2 . Star wars VII The Force Awakens is the most Gross movie."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "eca2c7eb",
   "metadata": {},
   "source": [
    "##  Maximum movies released in - "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "id": "558fe28b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "g=sns.barplot(x=imdb['Released_Year'].value_counts()[:10].index,y=imdb['Released_Year'].value_counts()[:10])\n",
    "g.set_title(\"Maximum Series released in-\", weight = \"bold\")\n",
    "g.set_xlabel(\"Years\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d3ce281c",
   "metadata": {},
   "source": [
    "### Insights\n",
    "1 . the above bargraph shows the most Maximum movies released.\n",
    "\n",
    "2 . In 2014 most of the movies are released"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f23bf214",
   "metadata": {},
   "source": [
    "###  Directors with most movies (lineplot)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "d0f81b38",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "g=sns.lineplot(x=imdb['Director'].value_counts()[:10].index,y=imdb['Released_Year'].value_counts()[:10])\n",
    "g.set_title(\"Mostly Occurred Directors\", weight = \"bold\")\n",
    "g.set_xlabel(\"Directors\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bb986f05",
   "metadata": {},
   "source": [
    "##  Directors with most movies(barplot)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "bb1bd403",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "g=sns.barplot(x=imdb['Director'].value_counts()[:10].index,y=imdb['Director'].value_counts()[:10])\n",
    "g.set_title(\"Mostly Occurred Directors\", weight = \"bold\")\n",
    "g.set_xlabel(\"Directors\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "70b23cb8",
   "metadata": {},
   "source": [
    "### Insights\n",
    "1 . the above bargraph shows the Directors on x-axis and number of movies on Y-axis .\n",
    "\n",
    "2 . Steven spielberg directed more movies compared to others"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1a6e0f4c",
   "metadata": {},
   "source": [
    "### Runtime of movies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "2cb3a24c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, 'Time Duration of movies')"
      ]
     },
     "execution_count": 66,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "g=sns.kdeplot(imdb['RunTime'])\n",
    "g.set_title(\"Time Duration of movies\", weight = \"bold\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "429a79da",
   "metadata": {},
   "source": [
    "### Insights\n",
    "\n",
    "1 . the above kdeplot shows the RunTime of Movies. \n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "65440a4e",
   "metadata": {},
   "source": [
    "###  Director Names"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 86,
   "id": "7e823600",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "imdb[\"Director\"].value_counts()[:10].plot.pie()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "60f60e3a",
   "metadata": {},
   "source": [
    "## Number of certified movies "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 104,
   "id": "e3a3cd03",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1224x432 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(17,6))\n",
    "imdb['certificate'].value_counts(ascending = True).plot(kind='barh')\n",
    "plt.title(\"certificate\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fe8839ff",
   "metadata": {},
   "source": [
    "### Insights \n",
    "\n",
    "1 . The above horizontal bargraph shows the most number of certified movies"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5773cb64",
   "metadata": {},
   "source": [
    "### IMDB Rating Distribution"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 121,
   "id": "3edcae64",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,axs=plt.subplots(figsize=(20,5))\n",
    "g=sns.distplot(imdb['Ratings'],bins=30)\n",
    "g.set_title(\"Distribution of Ratings\", weight = \"bold\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c856e2f1",
   "metadata": {},
   "source": [
    "## Insights\n",
    "\n",
    "1 . The above graph shows the top 500 most Rating Distribution\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "eab8e5c6",
   "metadata": {},
   "source": [
    "### Appearence of stars in top metaScore"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "c8d8331a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1224x504 with 4 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "stars=['Star1','Star2','Star3','Star4']\n",
    "fig,axs=plt.subplots(4,1,figsize=(17,7))\n",
    "ax=0\n",
    "for x in stars:\n",
    "    s=imdb.groupby([x]).sum().reset_index()\n",
    "    d=s.sort_values(['MetaScore']     ,ascending=False)[:10]\n",
    "    axs[ax].bar(d[x],d['MetaScore'])\n",
    "    axs[ax].set_title(x)\n",
    "    axs[ax].set_ylabel(\"Appearances\", weight = \"bold\")\n",
    "    ax+=1\n",
    "    plt.tight_layout()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "73ccd5ed",
   "metadata": {},
   "source": [
    "## Insights\n",
    "1 . the above bargraph shows the top 10 stars with most most Score.\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c8cb5c3f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6cb00c67",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7e3e65a5",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "04929a9f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
