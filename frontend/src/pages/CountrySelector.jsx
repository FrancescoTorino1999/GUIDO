import React, { useState, useEffect, useRef } from 'react';
import './CountrySelector.css';
import ResultDisplay from '../components/ResultDisplay'; // Import the ResultDisplay component

const CountrySelector = () => {
  const [countries] = useState([
    "Albania", "Algeria", "Saudi Arabia", "United Arab Emirates", "Argentina",
    "Armenia", "Australia", "Austria", "Azerbaijan", "Bangladesh", "Belarus",
    "Belgium", "Belgium French", "Belgium Netherl", "Bosnia and Herzegovina",
    "Brazil", "Bulgaria", "Burkina Faso", "Canada", "Chile", "China", "Colombia",
    "Costa Rica", "Croatia", "Cyprus", "Czech Rep", "Denmark", "Dominican Rep",
    "Ecuador", "Egypt", "Ethiopia", "El Salvador", "Estonia", "Finland", "France",
    "Georgia", "Germany", "Ghana", "United Kingdom", "Greece", "Guatemala",
    "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Korea South",
    "Latvia", "Lithuania", "Luxembourg", "North Macedonia", "Malaysia", "Malta",
    "Mexico", "Moldova", "Montenegro", "Morocco", "Netherlands", "New Zealand",
    "Nigeria", "Norway", "Pakistan", "Panama", "Peru", "Philippines", "Poland",
    "Portugal", "Puerto Rico", "Romania", "Russia", "Saudi Arabia", "Serbia",
    "Singapore", "Slovakia", "Slovenia", "South Africa", "South Africa white",
    "Spain", "Suriname", "Sweden", "Switzerland", "Taiwan", "Tanzania", "Thailand",
    "Trinidad and Tobago", "Turkey", "U.S.A.", "Uganda", "Ukraine", "Uruguay",
    "Venezuela", "Vietnam", "Zambia"
  ]);

  const [selectedOptionMap, setSelectedOptionMap] = useState(new Map());
  const [isOptionsVisible, setIsOptionsVisible] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [currentCountry, setCurrentCountry] = useState('');
  const [participants, setParticipants] = useState(1);
  const [geoDistribution, setGeoDistribution] = useState(null);
  const [results, setResults] = useState({});
  const [errorMessage, setErrorMessage] = useState('');
  const optionsRef = useRef(null);
  const [searchTerm, setSearchTerm] = useState('');

  const openModal = (countryName) => {
    setCurrentCountry(countryName);
    setParticipants(1);
    setIsModalVisible(true);
  };

  const handleSelect = () => {
    setSelectedOptionMap(prevMap => new Map(prevMap.set(currentCountry, parseInt(participants))));
    setIsModalVisible(false);
  };

  const removeSelectedOption = (countryName) => {
    setSelectedOptionMap(prevMap => {
      const newMap = new Map(prevMap);
      newMap.delete(countryName);
      return newMap;
    });
  };

  const handleOutsideClick = (event) => {
    if (optionsRef.current && !optionsRef.current.contains(event.target)) {
      setIsOptionsVisible(false);
      setSearchTerm('');
    }
  };

  useEffect(() => {
    document.addEventListener('click', handleOutsideClick);
    return () => {
      document.removeEventListener('click', handleOutsideClick);
    };
  }, []);

  const formatContent = (content) => {
    return {
      'description': content['description:'],
      'dispersion_description': content['dispersion_description'],
      'effects': content['effects'],
      'dispersion_value': content['dispersion_value'],
      'value': content['value'],
      'metric_name': content['metric_name:']
    };
  };

  const formatTitle = (title) => {
    if (title === title.toUpperCase()) {
      return title; // If already uppercase, return as is (for abbreviations like IDV)
    }
    return title
      .replace(/_/g, ' ') // Replace underscores with spaces
      .replace(/\b\w/g, char => char.toUpperCase()); // Capitalize the first letter of each word
  };

  const sendRequest = () => {
    // trova elemento con classe .country-selector-page
    let attualmenteSelezionato = document.querySelectorAll(".country-selector-page");
    // aggiungi la classe expand-page
    attualmenteSelezionato[0].classList.add("expand_page");

    if (!selectedOptionMap.size || geoDistribution === null) {
      setErrorMessage('Please select at least one country and a geographical dispersion option.');
      return;
    }

    const entriesList = Array.from(selectedOptionMap.entries());

    let mappedArray = entriesList
      .map(([country, number]) => ({
        "number": number,
        "nationality": country,
      }));
    mappedArray.push({ "geographical_dispersion": geoDistribution });

    fetch("http://127.0.0.1:5005/resolve_intent", { // to do change the url to cadocs
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "entities":mappedArray})
    }).then(async response => {
      if (response.status !== 200) {
        alert("error")
      }
      else {
        let result = await response.json()
        console.log(result);
        setResults(result);
      }
    })
  };


  const resetPage = () => {
    setSelectedOptionMap(new Map());
    setIsOptionsVisible(false);
    setIsModalVisible(false);
    setCurrentCountry('');
    setParticipants(1);
    setGeoDistribution(null);
    setResults({});
    setErrorMessage('');
  };

  const handleKeyDown = (event) => {
    if (isOptionsVisible) {
      const key = event.key.toLowerCase();

      if (key === 'enter' && searchTerm) {
        const matchingCountry = countries.find(country => country.toLowerCase() === searchTerm.toLowerCase());
        if (matchingCountry) {
          openModal(matchingCountry);
        }
      } else if (key === 'backspace') {
        setSearchTerm(prev => prev.slice(0, -1));
      } else if (/^[a-z]$/i.test(key)) { // Only add valid letter keys to the search term
        setSearchTerm(prev => prev + key);
        const firstCountry = countries.find(country => country.toLowerCase().startsWith(searchTerm + key));
        if (firstCountry) {
          const optionElement = document.getElementById(firstCountry);
          if (optionElement) {
            optionElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        }
      }
    }
  };
  return (
    <div className="country-selector-page page">
      <div className="header-country">
        <h2>Country Selector</h2>
      </div>
      <div
        className="custom-select"
        onClick={() => setIsOptionsVisible(!isOptionsVisible)}
        ref={optionsRef}
        onKeyDown={handleKeyDown}
        tabIndex="0"
      >
        <div className="selected-values">
          {Array.from(selectedOptionMap.entries()).map(([country, number]) => (
            <div key={country} className="selected-value">
              <span>{country} ({number})</span>
              <button className="remove-button" onClick={(e) => {
                e.stopPropagation();
                removeSelectedOption(country);
              }}>
              </button>
            </div>
          ))}
          {!selectedOptionMap.size && 'Select countries'}
        </div>
        {isOptionsVisible && (
          <div className={`options ${isOptionsVisible ? 'active' : ''}`}>
            {countries.map(country => (
              <div
                key={country}
                id={country}
                className="option"
                onClick={() => selectedOptionMap.has(country) ? removeSelectedOption(country) : openModal(country)}
              >
                {country}
              </div>
            ))}
          </div>
        )}
        <button className="btn-primary" onClick={resetPage}>Reset</button>
      </div>

      {isModalVisible && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content">
            <span className="close" onClick={() => setIsModalVisible(false)}>&times;</span>
            <h2 className="modal-header">Select number of participants</h2>
            <p>Selected Country: {currentCountry}</p>
            <div className="modal-input">
              <label htmlFor="participantsInput">Number of participants:</label>
              <input
                type="number"
                id="participantsInput"
                min="1"
                value={participants}
                onChange={e => setParticipants(e.target.value)}
              />
              <span>{participants} participants</span>
            </div>
            <div className="modal-buttons">
              <button className="cancel-button compute-button" onClick={() => setIsModalVisible(false)}>Cancel</button>
              <button className="ok-button compute-button" onClick={handleSelect}>OK</button>
            </div>
          </div>
        </div>
      )}

      <div className="content-wrapper">
        <div className="geographical-question">
          <p>Is your team or development community geographically distributed (i.e., do its participants work from different locations scattered around the globe)?</p>
          <div className="radio-buttons-container">
            <label><input type="radio" name="geoDistribution" value="100" onChange={() => setGeoDistribution(100)} /> All members of the community work from different parts of the globe.</label>
            <label><input type="radio" name="geoDistribution" value="75" onChange={() => setGeoDistribution(75)} /> Almost all (about 75%) members of the community work from different parts of the globe.</label>
            <label><input type="radio" name="geoDistribution" value="50" onChange={() => setGeoDistribution(50)} /> Most (about 50%) of the members of the community work from different parts of the globe.</label>
            <label><input type="radio" name="geoDistribution" value="25" onChange={() => setGeoDistribution(25)} /> A small portion (about 25%) of the members of the community work from different parts of the globe.</label>
            <label><input type="radio" name="geoDistribution" value="0" onChange={() => setGeoDistribution(0)} /> All members of the community work in the same location.</label>
          </div>
        </div>
      </div>

      {errorMessage && <div className="error-message">{errorMessage}</div>}

      <div className="results-container">
        {Object.keys(results).map(key => (
          key !== 'null_values' && (
            <ResultDisplay
              key={key}
              title={formatTitle(results[key]['metric_name'] || key)}
              content={formatContent(results[key])}
            />
          )
        ))}
      </div>

      <div className="center-button-container">
        <button className="btn-primary" onClick={sendRequest}
                disabled={!selectedOptionMap.size || geoDistribution === null}>Compute
        </button>
      </div>
    </div>
  );
};
export default CountrySelector;
