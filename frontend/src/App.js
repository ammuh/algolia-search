import React from 'react';
import algoliasearch from 'algoliasearch/lite';
import {
  InstantSearch,
  Hits,
  SearchBox,
  Configure,
  DynamicWidgets,
  RefinementList,
  Pagination,
  Highlight
} from 'react-instantsearch-dom';
import PropTypes from 'prop-types';
import './App.css';

const searchClient = algoliasearch(process.env.ALGOLIA_APP_ID, process.env.ALGOLIA_SEARCH_API_KEY);

function App() {
  return (
    <div>
      <header className="header">
        <h1 className="header-title">
          <a href="/">hebbia</a>
        </h1>
        <p className="header-subtitle">
          using{' '}
          <a href="https://github.com/algolia/react-instantsearch">
            React InstantSearch
          </a>
        </p>
      </header>

      <div class="row"><div className="container">
        <form enctype="multipart/form-data" id="parseform" action="/upload" method="post">
          <input type="file" name="file" multiple />
          <input type="submit" value="Upload" />
          <div className="container">
            <textarea name="parse1" form="parseform"></textarea>
            <textarea name="parse2" form="parseform"></textarea>
          </div>
        </form>
      </div></div>
      <div class="row">
        <div class="column">
          <div className="container">
            <InstantSearch searchClient={searchClient} indexName="passages">
              <div className="search-panel">
                <div className="search-panel__filters">
                  <Configure facets={['*']} maxValuesPerFacet={20} />
                  <DynamicWidgets fallbackWidget={RefinementList}>
                  </DynamicWidgets>
                </div>

                <div className="search-panel__results">
                  <SearchBox
                    className="searchbox"
                    translations={{
                      placeholder: '',
                    }}
                  />
                  <Hits hitComponent={Hit} />

                  <div className="pagination">
                    <Pagination />
                  </div>
                </div>
              </div>
            </InstantSearch>
          </div>
        </div>
        <div class="column">
          <div className="container">
            <InstantSearch searchClient={searchClient} indexName="passages_exp">
              <div className="search-panel">
                <div className="search-panel__filters">
                  <Configure facets={['*']} maxValuesPerFacet={20} />
                  <DynamicWidgets fallbackWidget={RefinementList}>
                  </DynamicWidgets>
                </div>

                <div className="search-panel__results">
                  <SearchBox
                    className="searchbox"
                    translations={{
                      placeholder: '',
                    }}
                  />
                  <Hits hitComponent={Hit} />

                  <div className="pagination">
                    <Pagination />
                  </div>
                </div>
              </div>
            </InstantSearch></div></div>
      </div>


    </div>
  );
}

function Hit(props) {
  return (
    <article>
       <h1>
        <Highlight attribute="passage" hit={props.hit} />
      </h1>
      <p><i>{props.hit.filename}</i></p>
    </article>
  );
}

Hit.propTypes = {
  hit: PropTypes.object.isRequired,
};

export default App;
