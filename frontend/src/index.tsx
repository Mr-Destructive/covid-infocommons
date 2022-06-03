import ReactDOM from 'react-dom';
import "./main.css"
import GrantsTable from './components/GrantTable';

import { GrantsFilter, OrgNameFacet } from './components/GrantsFilter';
import { css, jsx, ThemeProvider } from '@emotion/react'
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { createTheme } from '@mui/material/styles';
import React, { Component } from "react";
import axios from "axios";
import DownloadIcon from '@mui/icons-material/Download';

const styles = {
    // See MUI Button CSS classes at https://mui.com/material-ui/api/button/
    "&.MuiButton-contained": {
	color: "#FFFFFF",
	backgroundColor: "#2C6BAC",
	minWidth: "max-content",
	whiteSpace: "nowrap"
    },
};

interface Grant {
    id: number
    title: string
    award_amount: number
    abstract: string
    award_id: string
    pi: string
    funder_name: string
}

interface AppState {
    data: Grant[]
    url: string
    totalCount: number
    pageIndex: number
    awardee_org_names: OrgNameFacet[]
    filter: Filter
}

interface Filter {
    nsf_directorate?: string
    start_date?: Date
    end_date?: Date
}

let url = ''
if (process.env.NODE_ENV == 'production') {
    url = "https://cic-apps.datascience.columbia.edu";
} else if (process.env.NODE_ENV == 'development') {
    url = "https://cice-dev.paas.cc.columbia.edu";
} else {
    url = "http://127.0.0.1:8000"
}

class App extends Component<any, AppState> {
    state:AppState = {
        data: [],
        url: url,
        totalCount: 0,
        pageIndex: 0,
        awardee_org_names: [],
        filter: {
        }
    }

    constructor(props:any) {
        super(props)
        this.pageChangeHandler = this.pageChangeHandler.bind(this)
        this.filterChangeHandler = this.filterChangeHandler.bind(this)
    }

    componentDidMount = () => {
        this.get_grants_data()
        this.get_org_name_facet()
    }

    searchHandler = (event:any) => {
        event.preventDefault()
        const keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        this.get_grants_data(keyword)
    }

    get_org_name_facet() {
        var url = this.state.url.concat('/search/facets?field=awardee_organization.name')
        axios.get(url).then(results => {
            this.setState({ awardee_org_names: results.data.aggregations.patterns.buckets })
        })
    }

    get_grants_data = (keyword?:string) => {
        var url = this.state.url.concat('/search/grants')
        var params: { [key: string]: any } = {};

        let from:number = 0

        if (this.state.pageIndex > 0) {
            from = (this.state.pageIndex * 20) + 1
        } 
        params.from = from

        if (!keyword) {
            keyword = (document.getElementById('outlined-search') as HTMLInputElement).value;
        }
        if (keyword && keyword.length > 0) {
            params.keyword = keyword
        }

        let property: keyof typeof this.state.filter
        for (property in this.state.filter) {
            if (this.state.filter[property]) {
                params[property] = this.state.filter[property]
            }
        }
        
        axios.get(url, {params: params}).then(results => {
            this.setState({ totalCount: results.data.hits.total.value })

            var newArray = results.data.hits.hits.map(function(val:any) {
                var pi_name = ''
                var funder_name = ''
                if (val['_source']['principal_investigator'] != null) {
                    pi_name = val['_source']['principal_investigator']['first_name'] + ' ' + val['_source']['principal_investigator']['last_name']
                }
                return {
                    id: val['_source']['id'],
                    title: val['_source']['title'],
                    award_id: val['_source']['award_id'],
                    pi: pi_name,
                    abstract: val['_source']['abstract'],
                    award_amount: val['_source']['award_amount'],
                    funder_name: ('name' in val['_source']['funder']) ? val['_source']['funder']['name'] : ''
                }
            })
            this.setState({ data: newArray })
        })
    }

    downloadFile = (data:any, fileName:any, fileType:any) => {
        const blob = new Blob([data], { type: fileType })
        const a = document.createElement('a')
        a.download = fileName
        a.href = window.URL.createObjectURL(blob)
        const clickEvt = new MouseEvent('click', {
          view: window,
          bubbles: true,
          cancelable: true,
        })
        a.dispatchEvent(clickEvt)
        a.remove()
    }
      

    exportToCsv = (event:any) => {
        event.preventDefault()
        // Headers for each column
        let headers = ['Id,Title,Award_Amount,Award_ID,PI,Abstract,Funder']
        // Convert grants data to csv
        let grantsCsv = this.state.data.reduce((acc:any, grant:any) => {
            const grant_to_add:Grant = grant
            acc.push([
                grant_to_add.id,
                grant_to_add.title, 
                grant_to_add.award_amount,
                grant_to_add.award_id,
                grant_to_add.pi,
                grant_to_add.abstract,
                grant_to_add.funder_name
            ]
            .join(','))
            return acc
        }, [])
        this.downloadFile([...headers, ...grantsCsv].join('\n'), 'grants.csv', 'text/csv')
    }

    enterHandler = (e:any) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.get_grants_data()
        }
    }

    pageChangeHandler(page:number, pageSize: number) {
        this.setState({
            pageIndex: page
        })
        this.get_grants_data()
    }

    filterChangeHandler(fieldName:string, value:any) {
        var currentFilter = this.state.filter
        if (fieldName == 'nsf_directorate') {
            if (value) {
                currentFilter['nsf_directorate'] = value
            } else {
                delete currentFilter.nsf_directorate;
            }
        }
        if (fieldName == 'startDate') {
            if (value) {
                currentFilter['start_date'] = this.removeTime(value)
            } else {
                delete currentFilter.start_date;
            }
        }
        if (fieldName == 'endDate') {
            if (value) {
                currentFilter['end_date'] = this.removeTime(value)
            } else {
                delete currentFilter.end_date;
            }
        }
        console.log(currentFilter)
        this.setState({filter: currentFilter})
    }

    removeTime(date:Date) {
        return new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate()
        )
    }

    render() {
        return (
            <Box
                sx={{
                    width: '100%',
                    '& .MuiTextField-root': { width: '85%' },
                }}
                component="form"
                noValidate
                autoComplete="off"
            >
                <div className='root'>
                    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
                    <form className='search-form'>
                        <TextField
                            id="outlined-search" 
                            label="Search" 
                            type="search" 
                            onKeyDown={ this.enterHandler }/>

                        <Button
	                    sx={styles}
                            onClick={ this.searchHandler } 
                            className='search-button' 
                            variant="contained">Search</Button>
                    </form>
                    <br/>
                    <br/>
                    <div className='flex-container'>
                        <div className='flex-child'>
                            <GrantsTable
                                totalCount={ this.state.totalCount } 
                                data={ this.state.data} 
                                url={ this.state.url }
                                pageChangeHandler={ this.pageChangeHandler }
                                pageIndex={ this.state.pageIndex }
                            />
                </div>
                <div className='flex-child'>
                <div className='download-csv'>
                <Button sx={styles}
	                onClick={ this.exportToCsv } 
                        className='download-button' 
                        variant="contained"
            endIcon={ <DownloadIcon /> }>Download Results as CSV</Button>
                            </div>
                            <div>
                                <GrantsFilter
                                    awardee_org_names={ this.state.awardee_org_names }
                                    filterChangeHandler={ this.filterChangeHandler }
                                />
                            </div>
                        </div>
                </div>

                </div>
            </Box>
        );
    }
    
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
        
